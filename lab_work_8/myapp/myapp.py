"""Главное приложение с HTTPServer и маршрутизацией запросов.

Реализует архитектуру MVC для управления курсами валют.
Содержит контроллер для обработки HTTP запросов и рендеринга Jinja2 шаблонов.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, List, Any, Optional
from urllib.parse import parse_qs, urlparse
from jinja2 import Environment, PackageLoader, select_autoescape
import json
import threading
from datetime import datetime

from myapp.models import Author, App, User, Currency, UserCurrency
from myapp.utils import get_currencies


# Инициализация Jinja2 окружения один раз при старте приложения
env: Environment = Environment(
    loader=PackageLoader("myapp", "templates"),
    autoescape=select_autoescape(),
)

# Загрузка шаблонов один раз
template_index: Any = env.get_template("index.html")
template_users: Any = env.get_template("users.html")
template_currencies: Any = env.get_template("currencies.html")
template_user_detail: Any = env.get_template("user_detail.html")
template_author: Any = env.get_template("author.html")


class CurrenciesServer(BaseHTTPRequestHandler):
    """Обработчик HTTP запросов для приложения.
    
    Реализует маршрутизацию запросов и рендеринг шаблонов.
    Обеспечивает взаимодействие между моделями и представлениями (MVC).
    """

    # Класс-уровень данные (общее состояние приложения)
    app_config: Optional["AppConfig"] = None
    users: Dict[int, User] = {}
    user_currencies: List[UserCurrency] = []
    currencies_cache: List[Dict[str, Any]] = []
    currencies_cache_lock: threading.Lock = threading.Lock()
    last_update: Optional[str] = None

    def do_GET(self) -> None:
        """Обрабатывает GET запросы.
        
        Маршрутизирует запросы на соответствующие обработчики
        в зависимости от пути (path) и query параметров.
        
        Поддерживаемые маршруты:
        - GET / — главная страница
        - GET /users — список пользователей
        - GET /user?id=... — информация о пользователе
        - GET /currencies — список валют
        - GET /author — информация об авторе
        """
        # Парсим URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        try:
            if path == "/":
                self._handle_index()
            elif path == "/users":
                self._handle_users()
            elif path == "/user":
                user_id = self._get_query_param(query_params, "id", int)
                if user_id is not None:
                    self._handle_user_detail(user_id)
                else:
                    self._handle_not_found()
            elif path == "/currencies":
                self._handle_currencies()
            elif path == "/author":
                self._handle_author()
            else:
                self._handle_not_found()
        except Exception as e:
            self._send_error_response(500, f"Внутренняя ошибка сервера: {str(e)}")

    def _handle_index(self) -> None:
        """Обрабатывает главную страницу (/)."""
        html_content = template_index.render(
            app_name=self.app_config.app.name,
            version=self.app_config.app.version,
            author_name=self.app_config.app.author.name,
            group=self.app_config.app.author.group,
        )
        self._send_response(html_content, 200)

    def _handle_users(self) -> None:
        """Обрабатывает страницу со списком пользователей (/users)."""
        html_content = template_users.render(
            app_name=self.app_config.app.name,
            users=list(self.users.values()),
        )
        self._send_response(html_content, 200)

    def _handle_user_detail(self, user_id: int) -> None:
        """Обрабатывает страницу деталей пользователя (/user?id=...).
        
        Args:
            user_id: ID пользователя для отображения.
        """
        if user_id not in self.users:
            error = "Пользователь не найден"
            html_content = template_user_detail.render(
                app_name=self.app_config.app.name,
                error=error,
            )
            self._send_response(html_content, 404)
            return

        user = self.users[user_id]

        # Получаем валюты, на которые подписан пользователь
        user_currency_ids = [
            uc.currency_id
            for uc in self.user_currencies
            if uc.user_id == user_id
        ]

        user_currencies = [
            c for c in self.currencies_cache
            if c["id"] in user_currency_ids
        ]

        html_content = template_user_detail.render(
            app_name=self.app_config.app.name,
            user=user,
            user_currencies=user_currencies,
        )
        self._send_response(html_content, 200)

    def _handle_currencies(self) -> None:
        """Обрабатывает страницу со списком валют (/currencies)."""
        error = None

        # Если кэш пуст, пытаемся получить валюты
        if not self.currencies_cache:
            try:
                with self.currencies_cache_lock:
                    currencies_data = get_currencies()
                    self.currencies_cache = currencies_data
                    self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                error = f"Не удаётся получить данные о валютах: {str(e)}"

        html_content = template_currencies.render(
            app_name=self.app_config.app.name,
            currencies=self.currencies_cache,
            error=error,
            last_updated=self.last_update,
        )
        self._send_response(html_content, 200)

    def _handle_author(self) -> None:
        """Обрабатывает страницу с информацией об авторе (/author)."""
        html_content = template_author.render(
            app_name=self.app_config.app.name,
            version=self.app_config.app.version,
            author_name=self.app_config.app.author.name,
            group=self.app_config.app.author.group,
        )
        self._send_response(html_content, 200)

    def _handle_not_found(self) -> None:
        """Обрабатывает несуществующие маршруты (404)."""
        error_html = """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Ошибка 404</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    margin: 0;
                }
                .error-container {
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                }
                h1 { color: #c62828; font-size: 3em; margin: 0; }
                p { color: #666; font-size: 1.2em; margin: 20px 0; }
                a { color: #667eea; text-decoration: none; font-weight: 600; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="error-container">
                <h1>404</h1>
                <p>Страница не найдена</p>
                <p><a href="/">← Вернуться на главную</a></p>
            </div>
        </body>
        </html>
        """
        self._send_response(error_html, 404)

    def _send_response(self, content: str, status_code: int = 200) -> None:
        """Отправляет HTTP ответ с HTML контентом.
        
        Args:
            content: HTML содержимое ответа.
            status_code: HTTP статус код (по умолчанию 200).
        """
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(content.encode("utf-8")))
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def _send_error_response(self, status_code: int, message: str) -> None:
        """Отправляет HTTP ошибку.
        
        Args:
            status_code: HTTP статус код ошибки.
            message: Сообщение об ошибке.
        """
        error_html = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Ошибка {status_code}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    margin: 0;
                }}
                .error-container {{
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                }}
                h1 {{ color: #c62828; font-size: 3em; margin: 0; }}
                p {{ color: #666; font-size: 1.2em; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <h1>{status_code}</h1>
                <p>{message}</p>
            </div>
        </body>
        </html>
        """
        self._send_response(error_html, status_code)

    def log_message(self, format: str, *args: Any) -> None:
        """Переопределяет логирование для подавления вывода в консоль.
        
        Args:
            format: Строка формата для логирования.
            *args: Аргументы для подстановки в строку формата.
        """
        pass  # Подавляем логирование

    @staticmethod
    def _get_query_param(
        query_params: Dict[str, List[str]],
        param_name: str,
        param_type: type = str,
    ) -> Optional[Any]:
        """Получает параметр query строки с преобразованием типа.
        
        Args:
            query_params: Словарь параметров из parse_qs.
            param_name: Имя параметра.
            param_type: Тип для преобразования значения.
            
        Returns:
            Значение параметра преобразованное в param_type или None.
        """
        if param_name not in query_params:
            return None

        try:
            value = query_params[param_name][0]
            return param_type(value)
        except (IndexError, ValueError, TypeError):
            return None


class AppConfig:
    """Конфигурация приложения.
    
    Содержит информацию об приложении и авторе.
    
    Атрибуты:
        app: Объект App с информацией о приложении.
    """

    def __init__(self, app: App) -> None:
        """Инициализирует конфигурацию приложения.
        
        Args:
            app: Объект App.
        """
        self.app = app


def init_sample_data() -> None:
    """Инициализирует примеры данных для демонстрации.
    
    Создает образцы пользователей и их подписок на валюты.
    """
    # Создаем примеры пользователей
    users_data = [
        (1, "Иван Петров"),
        (2, "Анна Смирнова"),
        (3, "Сергей Волков"),
        (4, "Мария Соколова"),
        (5, "Дмитрий Лебедев"),
    ]

    for user_id, user_name in users_data:
        CurrenciesServer.users[user_id] = User(user_id, user_name)

    # Создаем примеры подписок (каждый пользователь подписан на 2-3 валюты)
    subscriptions = [
        (1, 1, "R01235"),  # USD
        (2, 1, "R01239"),  # EUR
        (3, 2, "R01235"),  # USD
        (4, 2, "R01240"),  # GBP
        (5, 3, "R01239"),  # EUR
        (6, 3, "R01240"),  # GBP
        (7, 4, "R01235"),  # USD
        (8, 5, "R01239"),  # EUR
    ]

    for uc_id, user_id, currency_id in subscriptions:
        CurrenciesServer.user_currencies.append(
            UserCurrency(uc_id, user_id, currency_id)
        )


def main() -> None:
    """Главная функция для запуска сервера.
    
    Инициализирует конфигурацию приложения, примеры данных и запускает HTTP сервер.
    """
    # Создаём объект автора
    author = Author(name="Смирнов Вадим", group="P4150")

    # Создаём объект приложения
    app = App(name="CurrenciesListApp", version="1.0.0", author=author)

    # Создаём конфигурацию приложения и устанавливаем её в класс
    config = AppConfig(app)
    CurrenciesServer.app_config = config

    # Инициализируем примеры данных
    init_sample_data()

    # Загружаем валюты при старте (опционально)
    try:
        with CurrenciesServer.currencies_cache_lock:
            currencies_data = get_currencies()
            CurrenciesServer.currencies_cache = currencies_data
            CurrenciesServer.last_update = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        print("Валюты успешно загружены")
    except Exception as e:
        print(f"Не удаётся загрузить валюты при старте: {e}")

    # Создаём HTTP сервер
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, CurrenciesServer)


    print(f"Сервер запущен на http://localhost:8000")
    print(f"Главная страница: http://localhost:8000/")
    print(f"Пользователи: http://localhost:8000/users")
    print(f"Валюты: http://localhost:8000/currencies")
    print(f"Об авторе: http://localhost:8000/author")


    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nСервер остановлен")
        httpd.server_close()


if __name__ == "__main__":
    main()

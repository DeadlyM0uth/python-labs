"""Главное приложение с HTTPServer и маршрутизацией запросов.

Реализует архитектуру MVC для управления курсами валют.
Содержит контроллер для обработки HTTP запросов и интеграцию всех
компонентов MVC (models, controllers, views).

Маршруты:
    GET /                   - Главная страница
    GET /users             - Список пользователей
    GET /user?id=...       - Информация о пользователе
    GET /currencies        - Список валют
    GET /currency/delete?id=... - Удаление валюты
    GET /currency/update?<code>=... - Обновление курса валюты
    GET /currency/show     - Вывод валют в консоль (отладка)
    GET /author            - Информация об авторе
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, List, Any, Optional
from urllib.parse import parse_qs, urlparse
from jinja2 import Environment, PackageLoader, select_autoescape
import io
import sys
import threading
from datetime import datetime

from myapp.models import Author, App, User, Currency, UserCurrency
from myapp.utils import get_currencies
from myapp.controllers.database_controller import CurrencyRatesCRUD
from myapp.controllers.currency_controller import CurrencyController
from myapp.controllers.pages import PageRenderer


# Инициализация Jinja2 окружения один раз при старте приложения
env: Environment = Environment(
    loader=PackageLoader("myapp", "templates"),
    autoescape=select_autoescape(),
)

# Инициализация page renderer
page_renderer: Optional[PageRenderer] = None


class CurrenciesServer(BaseHTTPRequestHandler):
    """Обработчик HTTP запросов для приложения.
    
    Реализует маршрутизацию GET запросов и интеграцию контроллеров MVC.
    Обеспечивает взаимодействие между database, business logic и view layers.
    """

    # Класс-уровень данные (общее состояние приложения)
    app_config: Optional["AppConfig"] = None
    currency_controller: Optional[CurrencyController] = None
    page_renderer: Optional[PageRenderer] = None

    def do_GET(self) -> None:
        """Обрабатывает GET запросы.
        
        Маршрутизирует запросы на соответствующие обработчики
        в зависимости от пути (path) и query параметров.
        
        Поддерживаемые маршруты:
            GET /                       - Главная страница
            GET /users                  - Список пользователей
            GET /user?id=...            - Информация о пользователе
            GET /currencies             - Список валют из БД
            GET /currency/delete?id=... - Удаление валюты
            GET /currency/update?<code>=... - Обновление курса валюты
            GET /currency/show          - Вывод валют в консоль
            GET /author                 - Информация об авторе
        """
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
                self._handle_currencies_db()
            elif path == "/currency/delete":
                currency_id = self._get_query_param(query_params, "id", int)
                if currency_id is not None:
                    self._handle_currency_delete(currency_id)
                else:
                    self._handle_not_found()
            elif path == "/currency/update":
                self._handle_currency_update(query_params)
            elif path == "/currency/show":
                self._handle_currency_show()
            elif path == "/author":
                self._handle_author()
            else:
                self._handle_not_found()
        except Exception as e:
            error_html = self.page_renderer.render_error(
                500,
                f"Внутренняя ошибка сервера: {str(e)}"
            )
            self._send_response(error_html, 500)

    def _handle_index(self) -> None:
        """Обрабатывает главную страницу (/)."""
        html_content = self.page_renderer.render_index(
            app_name=self.app_config.app.name,
            version=self.app_config.app.version,
            author_name=self.app_config.app.author.name,
            group=self.app_config.app.author.group,
        )
        self._send_response(html_content, 200)

    def _handle_users(self) -> None:
        """Обрабатывает страницу со списком пользователей (/users)."""
        users = self.currency_controller.list_users()
        html_content = self.page_renderer.render_users(
            app_name=self.app_config.app.name,
            users=users,
        )
        self._send_response(html_content, 200)

    def _handle_user_detail(self, user_id: int) -> None:
        """Обрабатывает страницу деталей пользователя (/user?id=...).
        
        Args:
            user_id: ID пользователя для отображения.
        """
        user = self.currency_controller.get_user(user_id)
        if not user:
            error = "Пользователь не найден"
            html_content = self.page_renderer.render_user_detail(
                app_name=self.app_config.app.name,
                error=error,
            )
            self._send_response(html_content, 404)
            return

        user_currencies = self.currency_controller.get_user_currencies(user_id)

        html_content = self.page_renderer.render_user_detail(
            app_name=self.app_config.app.name,
            user=user,
            user_currencies=user_currencies,
        )
        self._send_response(html_content, 200)

    def _handle_currencies_db(self) -> None:
        """Обрабатывает страницу со списком валют из БД (/currencies)."""
        currencies = self.currency_controller.list_currencies()
        error = None

        html_content = self.page_renderer.render_currencies(
            app_name=self.app_config.app.name,
            currencies=currencies,
            error=error,
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        self._send_response(html_content, 200)

    def _handle_currency_delete(self, currency_id: int) -> None:
        """Обрабатывает удаление валюты (/currency/delete?id=...).
        
        Args:
            currency_id: ID валюты для удаления.
        """
        success = self.currency_controller.delete_currency(currency_id)
        
        if success:
            message = f"Валюта с ID {currency_id} успешно удалена"
            html_content = self.page_renderer.render_success_message(message)
            self._send_response(html_content, 200)
        else:
            error = f"Валюта с ID {currency_id} не найдена"
            html_content = self.page_renderer.render_error(404, error)
            self._send_response(html_content, 404)

    def _handle_currency_update(self, query_params: Dict[str, List[str]]) -> None:
        """Обрабатывает обновление курса валюты (/currency/update?<code>=...).
        
        Ожидается передача параметра с кодом валюты и значением, например:
        /currency/update?USD=95.5
        
        Args:
            query_params: Параметры query строки.
        """
        # Получаем первый параметр (ключ и значение)
        for param_name in query_params:
            if param_name.upper() in ['ID', 'REDIR']:
                continue
            
            try:
                new_value = float(query_params[param_name][0])
                success = self.currency_controller.update_currency_value_by_code(
                    param_name.upper(),
                    new_value
                )
                
                if success:
                    message = f"Курс валюты {param_name.upper()} обновлен до {new_value}"
                    html_content = self.page_renderer.render_success_message(message)
                    self._send_response(html_content, 200)
                else:
                    error = f"Валюта {param_name.upper()} не найдена"
                    html_content = self.page_renderer.render_error(404, error)
                    self._send_response(html_content, 404)
                return
            except ValueError:
                error = f"Некорректное значение курса: {query_params[param_name][0]}"
                html_content = self.page_renderer.render_error(400, error)
                self._send_response(html_content, 400)
                return
        
        error = "Не указана валюта для обновления"
        html_content = self.page_renderer.render_error(400, error)
        self._send_response(html_content, 400)

    def _handle_currency_show(self) -> None:
        """Обрабатывает вывод валют в консоль для отладки (/currency/show)."""
        currencies = self.currency_controller.list_currencies()
        
        # Перенаправляем stdout для захвата вывода print
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        print("=" * 80)
        print("СПИСОК ВАЛЮТ В БД:")
        print("=" * 80)
        
        if not currencies:
            print("В базе данных нет валют.")
        else:
            for currency in currencies:
                print(
                    f"ID: {currency['id']}, "
                    f"NumCode: {currency['num_code']}, "
                    f"CharCode: {currency['char_code']}, "
                    f"Name: {currency['name']}, "
                    f"Value: {currency['value']}, "
                    f"Nominal: {currency['nominal']}"
                )
        
        print("=" * 80)
        
        # Восстанавливаем stdout
        output = buffer.getvalue()
        sys.stdout = old_stdout
        
        # Выводим в консоль
        print(output)
        
        # Отправляем успешный ответ
        message = f"Выведено {len(currencies)} валют(ы) в консоль"
        html_content = self.page_renderer.render_success_message(message)
        self._send_response(html_content, 200)

    def _handle_author(self) -> None:
        """Обрабатывает страницу с информацией об авторе (/author)."""
        html_content = self.page_renderer.render_author(
            app_name=self.app_config.app.name,
            version=self.app_config.app.version,
            author_name=self.app_config.app.author.name,
            group=self.app_config.app.author.group,
        )
        self._send_response(html_content, 200)

    def _handle_not_found(self) -> None:
        """Обрабатывает несуществующие маршруты (404)."""
        error_html = self.page_renderer.render_error_404()
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

    def log_message(self, format: str, *args: Any) -> None:
        """Переопределяет логирование для подавления вывода в консоль.
        
        Args:
            format: Строка формата для логирования.
            *args: Аргументы для подстановки в строку формата.
        """
        pass

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
    
    Содержит информацию о приложении и авторе.
    
    Attributes:
        app: Объект App с информацией о приложении.
    """

    def __init__(self, app: App) -> None:
        """Инициализирует конфигурацию приложения.
        
        Args:
            app: Объект App.
        """
        self.app = app


def main() -> None:
    """Главная функция для запуска сервера.
    
    Инициализирует:
    - Объект приложения (App) и конфигурацию
    - Контроллер базы данных SQLite в памяти
    - Бизнес-логику контроллера (CurrencyController)
    - Renderer для Jinja2 шаблонов (PageRenderer)
    - HTTP сервер с маршрутизацией
    
    Загружает примеры данных и запускает сервер на порту 8000.
    """
    # Создаём объект автора
    author = Author(name="Смирнов Вадим", group="P4150")

    # Создаём объект приложения
    app = App(name="CurrenciesListApp", version="2.0.0", author=author)

    # Создаём конфигурацию приложения
    config = AppConfig(app)

    # Инициализируем контроллеры
    db_controller = CurrencyRatesCRUD(db_path=':memory:')
    currency_controller = CurrencyController(db_controller)
    page_renderer_instance = PageRenderer(env)

    # Устанавливаем контроллеры в класс обработчика
    CurrenciesServer.app_config = config
    CurrenciesServer.currency_controller = currency_controller
    CurrenciesServer.page_renderer = page_renderer_instance

    # Инициализируем примеры данных в БД
    _init_sample_data(currency_controller)

    # Создаём HTTP сервер
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, CurrenciesServer)

    print("=" * 80)
    print("Сервер запущен на http://localhost:8000")
    print("=" * 80)
    print(f"Главная страница:       http://localhost:8000/")
    print(f"Пользователи:           http://localhost:8000/users")
    print(f"Валюты (из БД):         http://localhost:8000/currencies")
    print(f"Об авторе:              http://localhost:8000/author")
    print()
    print("CRUD операции:")
    print(f"Удалить валюту:         http://localhost:8000/currency/delete?id=1")
    print(f"Обновить курс:          http://localhost:8000/currency/update?USD=95.5")
    print(f"Показать валюты (логи): http://localhost:8000/currency/show")
    print("=" * 80)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nСервер остановлен")
        db_controller.close()
        httpd.server_close()


def _init_sample_data(controller: CurrencyController) -> None:
    """Инициализирует примеры данных в базе данных.
    
    Создает пользователей, валюты и подписки для демонстрации.
    
    Args:
        controller: Экземпляр CurrencyController.
    """
    # Создаем пользователей
    users_data = [
        "Иван Петров",
        "Анна Смирнова",
        "Сергей Волков",
        "Мария Соколова",
        "Дмитрий Лебедев",
    ]

    user_ids = []
    for user_name in users_data:
        user_id = controller.add_user(user_name)
        user_ids.append(user_id)

    # Создаем валюты
    currencies_data = [
        ("840", "USD", "Доллар США", 90.0, 1),
        ("978", "EUR", "Евро", 91.0, 1),
        ("826", "GBP", "Британский фунт", 110.0, 1),
        ("392", "JPY", "Японская йена", 0.7, 100),
        ("156", "CNY", "Китайский юань", 12.5, 1),
    ]

    currency_ids = []
    for num_code, char_code, name, value, nominal in currencies_data:
        currency_id = controller.add_currency(
            num_code, char_code, name, value, nominal
        )
        currency_ids.append(currency_id)

    # Создаем подписки пользователей на валюты
    subscriptions = [
        (0, 0),  # User 1 -> USD
        (0, 1),  # User 1 -> EUR
        (1, 0),  # User 2 -> USD
        (1, 2),  # User 2 -> GBP
        (2, 1),  # User 3 -> EUR
        (2, 2),  # User 3 -> GBP
        (3, 0),  # User 4 -> USD
        (4, 1),  # User 5 -> EUR
    ]

    for user_idx, currency_idx in subscriptions:
        try:
            controller.subscribe_user_to_currency(
                user_ids[user_idx],
                currency_ids[currency_idx]
            )
        except Exception:
            pass  # Игнорируем ошибки при подписке


if __name__ == "__main__":
    main()


"""Контроллер представлений для рендеринга шаблонов Jinja2.

Этот модуль реализует слой представлений в архитектуре MVC.
Отвечает за рендеринг HTML шаблонов с помощью Jinja2.
Отделяет презентационную логику от бизнес-логики и операций с базой данных.
"""

from typing import Dict, List, Any, Optional
from jinja2 import Environment, Template


class PageRenderer:
    """Контроллер для рендеринга HTML-страниц с использованием Jinja2.
    
    Предоставляет методы для рендеринга всех страниц приложения.
    Использует общий экземпляр Jinja2 Environment для повышения эффективности.
    
    Attributes:
        env: Jinja2 Environment для рендеринга шаблонов.
    """

    def __init__(self, env: Environment) -> None:
        """Инициализирует рендерер страниц.
        
        Args:
            env: Jinja2 Environment instance (should be created once and shared).
        """
        self.env: Environment = env
        self._preload_templates()

    def _preload_templates(self) -> None:
        """Предзагружает часто используемые шаблоны для повышения производительности.
        
        Загружает шаблоны при инициализации, чтобы избежать многократных операций ввода-вывода.
        """
        try:
            self.template_index: Template = self.env.get_template("index.html")
            self.template_users: Template = self.env.get_template("users.html")
            self.template_currencies: Template = self.env.get_template(
                "currencies.html"
            )
            self.template_user_detail: Template = self.env.get_template(
                "user_detail.html"
            )
            self.template_author: Template = self.env.get_template("author.html")
        except Exception as e:
            raise RuntimeError(f"Failed to load templates: {str(e)}") from e

    def render_index(
        self,
        app_name: str,
        version: str,
        author_name: str,
        group: str
    ) -> str:
        """Отображает главную страницу (index).
        
        Args:
            app_name: Название приложения.
            version: Версия приложения.
            author_name: Имя автора.
            group: Учебная группа автора.
        
        Returns:
            Сформированный HTML в виде строки.
        """
        return self.template_index.render(
            app_name=app_name,
            version=version,
            author_name=author_name,
            group=group,
        )

    def render_users(
        self,
        app_name: str,
        users: List[Dict[str, Any]]
    ) -> str:
        """Отображает страницу со списком пользователей.
        
        Args:
            app_name: Название приложения.
            users: Список словарей пользователей.
        
        Returns:
            Сформированный HTML в виде строки.
        """
        return self.template_users.render(
            app_name=app_name,
            users=users,
        )

    def render_currencies(
        self,
        app_name: str,
        currencies: List[Dict[str, Any]],
        error: Optional[str] = None,
        last_updated: Optional[str] = None
    ) -> str:
        """Отображает страницу со списком валют.
        
        Args:
            app_name: Название приложения.
            currencies: Список словарей валют.
            error: Сообщение об ошибке (если есть).
            last_updated: Временная метка последнего обновления.
        
        Returns:
            Сформированный HTML в виде строки.
        """
        return self.template_currencies.render(
            app_name=app_name,
            currencies=currencies,
            error=error,
            last_updated=last_updated,
        )

    def render_user_detail(
        self,
        app_name: str,
        user: Optional[Dict[str, Any]] = None,
        user_currencies: Optional[List[Dict[str, Any]]] = None,
        error: Optional[str] = None
    ) -> str:
        """Отображает страницу с деталями пользователя.
        
        Args:
            app_name: Название приложения.
            user: Словарь пользователя или None, если пользователь не найден.
            user_currencies: Список валют, на которые подписан пользователь.
            error: Сообщение об ошибке (если есть).
        
        Returns:
            Сформированный HTML в виде строки.
        """
        return self.template_user_detail.render(
            app_name=app_name,
            user=user,
            user_currencies=user_currencies or [],
            error=error,
        )

    def render_author(
        self,
        app_name: str,
        version: str,
        author_name: str,
        group: str
    ) -> str:
        """Отображает страницу с информацией об авторе.
        
        Args:
            app_name: Название приложения.
            version: Версия приложения.
            author_name: Имя автора.
            group: Учебная группа автора.
        
        Returns:
            Сформированный HTML в виде строки.
        """
        return self.template_author.render(
            app_name=app_name,
            version=version,
            author_name=author_name,
            group=group,
        )

    @staticmethod
    def render_error_404() -> str:
        """Отображает страницу ошибки 404 (не найдено).
        
        Returns:
            Сформированный HTML в виде строки.
        """
        return """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Ошибка 404</title>
        </head>
        <body>
            <div">
                <h1>404</h1>
                <p>Страница не найдена</p>
                <p><a href="/">Вернуться на главную</a></p>
            </div>
        </body>
        </html>
        """

    @staticmethod
    def render_error(status_code: int, message: str) -> str:
        """Отображает страницу с общей ошибкой.
        
        Args:
            status_code: HTTP код ошибки.
            message: Сообщение об ошибке для отображения.
        
        Returns:
            Сформированный HTML в виде строки.
        """
        return f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Ошибка {status_code}</title>
        </head>
        <body>
            <div">
                <h1>{status_code}</h1>
                <p>{message}</p>
            </div>
        </body>
        </html>
        """

    @staticmethod
    def render_success_message(message: str) -> str:
        """Отображает страницу с сообщением об успешной операции.
        
        Args:
            message: Сообщение об успешной операции для отображения.
        
        Returns:
            Сформированный HTML в виде строки.
        """
        return f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Успешно</title>
        </head>
        <body>
            <div">
                <h1>Успешно</h1>
                <p>{message}</p>
                <p><a href="/">Вернуться на главную</a></p>
            </div>
        </body>
        </html>
        """

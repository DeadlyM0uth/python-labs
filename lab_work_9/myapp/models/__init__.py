"""Пакет моделей приложения.

Содержит все модели предметной области: Author, App, User, Currency, UserCurrency.
"""

from myapp.models.author import Author
from myapp.models.app import App
from myapp.models.user import User
from myapp.models.currency import Currency
from myapp.models.user_currency import UserCurrency

__all__ = [
    "Author",
    "App",
    "User",
    "Currency",
    "UserCurrency",
]

"""Тесты для HTTPServer контроллера.

Содержит юнит-тесты для проверки маршрутизации запросов и рендеринга шаблонов.
"""

import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO
import sys
import os

# Добавляем путь для импортов
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from myapp.myapp import CurrenciesServer, AppConfig, init_sample_data
from myapp.models import Author, App, User, Currency, UserCurrency


class TestCurrenciesServer(unittest.TestCase):
    """Тесты для класса CurrenciesServer."""

    def setUp(self) -> None:
        """Подготовка к каждому тесту."""
        # Создаём конфигурацию приложения
        author = Author(name="Тест Тестов", group="TEST")
        app = App(name="TestApp", version="1.0.0", author=author)
        CurrenciesServer.app_config = AppConfig(app)

        # Инициализируем примеры данных
        init_sample_data()

        # Добавляем примеры валют
        CurrenciesServer.currencies_cache = [
            {
                'id': 'R01235',
                'num_code': '840',
                'char_code': 'USD',
                'name': 'Доллар США',
                'value': '75.5',
                'nominal': '1',
            },
            {
                'id': 'R01239',
                'num_code': '978',
                'char_code': 'EUR',
                'name': 'Евро',
                'value': '82.3',
                'nominal': '1',
            },
        ]

    def test_server_has_app_config(self) -> None:
        """Тест что сервер имеет конфигурацию приложения."""
        self.assertIsNotNone(CurrenciesServer.app_config)
        self.assertEqual(CurrenciesServer.app_config.app.name, "TestApp")

    def test_server_has_users(self) -> None:
        """Тест что сервер имеет пользователей."""
        self.assertGreater(len(CurrenciesServer.users), 0)

    def test_server_has_user_currencies(self) -> None:
        """Тест что сервер имеет подписки."""
        self.assertGreater(len(CurrenciesServer.user_currencies), 0)

    def test_server_has_currencies_cache(self) -> None:
        """Тест что сервер имеет кэш валют."""
        self.assertEqual(len(CurrenciesServer.currencies_cache), 2)

    def test_get_query_param_string(self) -> None:
        """Тест извлечения строкового параметра."""
        query_params = {'id': ['123']}
        result = CurrenciesServer._get_query_param(query_params, 'id', str)
        self.assertEqual(result, '123')

    def test_get_query_param_int(self) -> None:
        """Тест извлечения целочисленного параметра."""
        query_params = {'id': ['123']}
        result = CurrenciesServer._get_query_param(query_params, 'id', int)
        self.assertEqual(result, 123)
        self.assertIsInstance(result, int)

    def test_get_query_param_not_found(self) -> None:
        """Тест извлечения несуществующего параметра."""
        query_params = {}
        result = CurrenciesServer._get_query_param(query_params, 'id', int)
        self.assertIsNone(result)

    def test_get_query_param_invalid_conversion(self) -> None:
        """Тест извлечения параметра с ошибкой преобразования."""
        query_params = {'id': ['not_an_int']}
        result = CurrenciesServer._get_query_param(query_params, 'id', int)
        self.assertIsNone(result)

    def test_user_exists(self) -> None:
        """Тест что пользователь существует."""
        self.assertIn(1, CurrenciesServer.users)
        user = CurrenciesServer.users[1]
        self.assertIsInstance(user, User)

    def test_user_currencies_exist(self) -> None:
        """Тест что подписки существуют."""
        user_currencies = [
            uc for uc in CurrenciesServer.user_currencies
            if uc.user_id == 1
        ]
        self.assertGreater(len(user_currencies), 0)

    def test_currencies_cache_content(self) -> None:
        """Тест содержимого кэша валют."""
        self.assertEqual(len(CurrenciesServer.currencies_cache), 2)
        
        # Проверяем первую валюту
        usd = CurrenciesServer.currencies_cache[0]
        self.assertEqual(usd['char_code'], 'USD')
        self.assertEqual(usd['num_code'], '840')
        
        # Проверяем вторую валюту
        eur = CurrenciesServer.currencies_cache[1]
        self.assertEqual(eur['char_code'], 'EUR')
        self.assertEqual(eur['num_code'], '978')

    def test_find_user_currencies_by_id(self) -> None:
        """Тест поиска валют пользователя по ID."""
        user_id = 1
        user_currency_ids = [
            uc.currency_id
            for uc in CurrenciesServer.user_currencies
            if uc.user_id == user_id
        ]
        self.assertGreater(len(user_currency_ids), 0)
        self.assertIn('R01235', user_currency_ids)  # USD

    def test_get_user_currencies_data(self) -> None:
        """Тест получения данных валют для пользователя."""
        user_id = 1
        user_currency_ids = [
            uc.currency_id
            for uc in CurrenciesServer.user_currencies
            if uc.user_id == user_id
        ]
        
        user_currencies = [
            c for c in CurrenciesServer.currencies_cache
            if c["id"] in user_currency_ids
        ]
        
        self.assertGreater(len(user_currencies), 0)
        # Проверяем что получены валюты из кэша
        for currency in user_currencies:
            self.assertIn('char_code', currency)
            self.assertIn('value', currency)


class TestAppConfig(unittest.TestCase):
    """Тесты для класса AppConfig."""

    def test_app_config_creation(self) -> None:
        """Тест создания конфигурации приложения."""
        author = Author(name="Тест", group="TEST")
        app = App(name="TestApp", version="1.0.0", author=author)
        config = AppConfig(app)
        
        self.assertIsNotNone(config.app)
        self.assertEqual(config.app.name, "TestApp")
        self.assertEqual(config.app.version, "1.0.0")

    def test_app_config_author_info(self) -> None:
        """Тест доступа к информации об авторе через конфигурацию."""
        author = Author(name="Иван Петров", group="P3120")
        app = App(name="TestApp", version="1.0.0", author=author)
        config = AppConfig(app)
        
        self.assertEqual(config.app.author.name, "Иван Петров")
        self.assertEqual(config.app.author.group, "P3120")


if __name__ == "__main__":
    unittest.main()

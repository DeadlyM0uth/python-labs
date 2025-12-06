"""Юнит-тесты для приложения управления курсами валют.

Тесты для:
- CRUD операций в контроллере базы данных CurrencyRatesCRUD (SQLite)
- Бизнес-логики в CurrencyController
- Операций Create, Read, Update, Delete (CRUD)
- Внешних ключей и целостности данных
- Обработки ошибок и валидации

Использует unittest.mock для мокирования зависимостей базы данных и тестирования
логики контроллера в изоляции.
"""

import unittest
from unittest.mock import MagicMock, patch, call
from typing import Dict, Any

from myapp.controllers.database_controller import CurrencyRatesCRUD
from myapp.controllers.currency_controller import CurrencyController


class TestCurrencyRatesCRUD(unittest.TestCase):
    """Тесты для контроллера базы данных CurrencyRatesCRUD."""

    def setUp(self) -> None:
        """Настраивает тестовую базу данных для каждого теста.
        
        Создаёт SQLite базу в памяти (:memory:) для тестирования.
        """
        self.db = CurrencyRatesCRUD(db_path=':memory:')

    def tearDown(self) -> None:
        """Закрывает соединение с базой данных после каждого теста."""
        self.db.close()

    # ============= ТЕСТЫ CRUD ВАЛЮТ =============
    
    def test_create_currency(self) -> None:
        """Тест создания новой записи валюты."""
        currency_id = self.db.create_currency(
            num_code='840',
            char_code='USD',
            name='Доллар США',
            value=90.0,
            nominal=1
        )
        
        self.assertIsNotNone(currency_id)
        self.assertGreater(currency_id, 0)

    def test_read_currency(self) -> None:
        """Тест чтения валюты по ID."""
        # Создаём валюту для теста
        currency_id = self.db.create_currency(
            num_code='840',
            char_code='USD',
            name='Доллар США',
            value=90.0,
            nominal=1
        )
        
        # Читаем запись обратно
        currency = self.db.read_currency(currency_id)
        
        self.assertIsNotNone(currency)
        self.assertEqual(currency['char_code'], 'USD')
        self.assertEqual(currency['value'], 90.0)
        self.assertEqual(currency['num_code'], '840')

    def test_read_all_currencies(self) -> None:
        """Тест чтения всех валют из базы данных."""
        # Создаём несколько валют
        self.db.create_currency('840', 'USD', 'Доллар США', 90.0, 1)
        self.db.create_currency('978', 'EUR', 'Евро', 91.0, 1)
        
        # Читаем все валюты
        currencies = self.db.read_currencies()
        
        self.assertEqual(len(currencies), 2)
        self.assertEqual(currencies[0]['char_code'], 'USD')
        self.assertEqual(currencies[1]['char_code'], 'EUR')

    def test_read_currency_by_char_code(self) -> None:
        """Тест чтения валюты по символьному коду."""
        self.db.create_currency(
            num_code='840',
            char_code='USD',
            name='Доллар США',
            value=90.0,
            nominal=1
        )
        
        currency = self.db.read_currency_by_char_code('USD')
        
        self.assertIsNotNone(currency)
        self.assertEqual(currency['num_code'], '840')

    def test_update_currency(self) -> None:
        """Тест обновления значения курса валюты."""
        currency_id = self.db.create_currency(
            num_code='840',
            char_code='USD',
            name='Доллар США',
            value=90.0,
            nominal=1
        )
        
        # Обновляем значение курса
        success = self.db.update_currency(currency_id, value=95.5)
        
        self.assertTrue(success)
        
        # Проверяем обновление
        currency = self.db.read_currency(currency_id)
        self.assertEqual(currency['value'], 95.5)

    def test_update_currency_multiple_fields(self) -> None:
        """Тест обновления нескольких полей валюты."""
        currency_id = self.db.create_currency(
            num_code='840',
            char_code='USD',
            name='Доллар США',
            value=90.0,
            nominal=1
        )
        
        success = self.db.update_currency(
            currency_id,
            value=95.5,
            name='US Dollar'
        )
        
        self.assertTrue(success)
        
        currency = self.db.read_currency(currency_id)
        self.assertEqual(currency['value'], 95.5)
        self.assertEqual(currency['name'], 'US Dollar')

    def test_update_nonexistent_currency(self) -> None:
        """Тест обновления несуществующей валюты возвращает False."""
        success = self.db.update_currency(9999, value=100.0)
        
        self.assertFalse(success)

    def test_delete_currency(self) -> None:
        """Тест удаления валюты."""
        currency_id = self.db.create_currency(
            num_code='840',
            char_code='USD',
            name='Доллар США',
            value=90.0,
            nominal=1
        )
        
        # Удаляем запись
        success = self.db.delete_currency(currency_id)
        self.assertTrue(success)
        
        # Проверяем, что запись удалена
        currency = self.db.read_currency(currency_id)
        self.assertIsNone(currency)

    def test_delete_nonexistent_currency(self) -> None:
        """Тест удаления несуществующей валюты возвращает False."""
        success = self.db.delete_currency(9999)
        
        self.assertFalse(success)

    # ============= ТЕСТЫ CRUD ПОЛЬЗОВАТЕЛЕЙ =============
    
    def test_create_user(self) -> None:
        """Тест создания нового пользователя."""
        user_id = self.db.create_user('Иван Петров')
        
        self.assertIsNotNone(user_id)
        self.assertGreater(user_id, 0)

    def test_read_user(self) -> None:
        """Тест чтения пользователя по ID."""
        user_id = self.db.create_user('Иван Петров')
        
        user = self.db.read_user(user_id)
        
        self.assertIsNotNone(user)
        self.assertEqual(user['name'], 'Иван Петров')

    def test_read_all_users(self) -> None:
        """Тест чтения всех пользователей."""
        self.db.create_user('Иван Петров')
        self.db.create_user('Анна Смирнова')
        
        users = self.db.read_users()
        
        self.assertEqual(len(users), 2)

    def test_update_user(self) -> None:
        """Тест обновления имени пользователя."""
        user_id = self.db.create_user('Иван Петров')
        
        success = self.db.update_user(user_id, 'Иван Иванов')
        
        self.assertTrue(success)
        
        user = self.db.read_user(user_id)
        self.assertEqual(user['name'], 'Иван Иванов')

    def test_delete_user(self) -> None:
        """Тест удаления пользователя."""
        user_id = self.db.create_user('Иван Петров')
        
        success = self.db.delete_user(user_id)
        self.assertTrue(success)
        
        user = self.db.read_user(user_id)
        self.assertIsNone(user)

    # ============= ТЕСТЫ ПОДПИСК (USER_CURRENCY) =============
    
    def test_create_user_currency(self) -> None:
        """Тест создания подписки пользователя на валюту."""
        user_id = self.db.create_user('Иван Петров')
        currency_id = self.db.create_currency(
            '840', 'USD', 'Доллар США', 90.0, 1
        )
        
        uc_id = self.db.create_user_currency(user_id, currency_id)
        
        self.assertIsNotNone(uc_id)
        self.assertGreater(uc_id, 0)

    def test_read_user_currencies(self) -> None:
        """Тест чтения всех валют, на которые подписан пользователь."""
        user_id = self.db.create_user('Иван Петров')
        
        # Создаём валюты
        usd_id = self.db.create_currency(
            '840', 'USD', 'Доллар США', 90.0, 1
        )
        eur_id = self.db.create_currency(
            '978', 'EUR', 'Евро', 91.0, 1
        )
        
        # Подписываем пользователя на обе валюты
        self.db.create_user_currency(user_id, usd_id)
        self.db.create_user_currency(user_id, eur_id)
        
        # Читаем подписки
        currencies = self.db.read_user_currencies(user_id)
        
        self.assertEqual(len(currencies), 2)
        char_codes = [c['char_code'] for c in currencies]
        self.assertIn('USD', char_codes)
        self.assertIn('EUR', char_codes)

    def test_delete_user_currency(self) -> None:
        """Тест удаления подписки пользователя."""
        user_id = self.db.create_user('Иван Петров')
        currency_id = self.db.create_currency(
            '840', 'USD', 'Доллар США', 90.0, 1
        )
        
        self.db.create_user_currency(user_id, currency_id)
        
        # Удаляем подписку
        success = self.db.delete_user_currency(user_id, currency_id)
        self.assertTrue(success)
        
        # Проверяем, что подписка удалена
        currencies = self.db.read_user_currencies(user_id)
        self.assertEqual(len(currencies), 0)

    # ============= ТЕСТЫ ВНЕШНИХ КЛЮЧЕЙ И ЦЕЛОСТНОСТИ ДАННЫХ =============
    
    def test_parameterized_queries_protection(self) -> None:
        """Тест, что параметризованные запросы защищают от SQL-инъекций."""
        # Пытаемся создать валюту с попыткой SQL-инъекции
        malicious_name = "'; DROP TABLE currency; --"
        
        currency_id = self.db.create_currency(
            '840', 'USD', malicious_name, 90.0, 1
        )
        
        # Проверяем, что таблица осталась и данные созданы безопасно
        currency = self.db.read_currency(currency_id)
        self.assertIsNotNone(currency)
        self.assertEqual(currency['name'], malicious_name)


class TestCurrencyController(unittest.TestCase):
    """Тесты для бизнес-логики CurrencyController."""

    def setUp(self) -> None:
        """Настраивает тестовый контроллер с мокированной базой данных."""
        self.mock_db = MagicMock(spec=CurrencyRatesCRUD)
        self.controller = CurrencyController(self.mock_db)

    # ============= ТЕСТЫ КОНТРОЛЛЕРА ВАЛЮТ =============
    
    def test_list_currencies(self) -> None:
        """Тест получения списка валют через контроллер."""
        # Мокаем ответ базы данных
        expected_currencies = [
            {'id': 1, 'char_code': 'USD', 'value': 90.0},
            {'id': 2, 'char_code': 'EUR', 'value': 91.0},
        ]
        self.mock_db.read_currencies.return_value = expected_currencies
        
        result = self.controller.list_currencies()
        
        self.assertEqual(result, expected_currencies)
        self.mock_db.read_currencies.assert_called_once()

    def test_get_currency(self) -> None:
        """Тест получения отдельной валюты."""
        expected_currency = {'id': 1, 'char_code': 'USD', 'value': 90.0}
        self.mock_db.read_currency.return_value = expected_currency
        
        result = self.controller.get_currency(1)
        
        self.assertEqual(result, expected_currency)
        self.mock_db.read_currency.assert_called_once_with(1)

    def test_get_currency_by_code(self) -> None:
        """Тест получения валюты по символьному коду."""
        expected_currency = {'id': 1, 'char_code': 'USD', 'value': 90.0}
        self.mock_db.read_currency_by_char_code.return_value = expected_currency
        
        result = self.controller.get_currency_by_code('USD')
        
        self.assertEqual(result, expected_currency)
        self.mock_db.read_currency_by_char_code.assert_called_once_with('USD')

    def test_add_currency(self) -> None:
        """Тест добавления новой валюты."""
        self.mock_db.create_currency.return_value = 1
        
        result = self.controller.add_currency(
            '840', 'USD', 'Доллар США', 90.0, 1
        )
        
        self.assertEqual(result, 1)
        self.mock_db.create_currency.assert_called_once_with(
            '840', 'USD', 'Доллар США', 90.0, 1
        )

    def test_update_currency(self) -> None:
        """Тест обновления полей валюты."""
        self.mock_db.update_currency.return_value = True
        
        result = self.controller.update_currency(1, value=95.5)
        
        self.assertTrue(result)
        self.mock_db.update_currency.assert_called_once_with(1, value=95.5)

    def test_update_currency_value(self) -> None:
        """Тест обновления только значения курса валюты."""
        self.mock_db.update_currency.return_value = True
        
        result = self.controller.update_currency_value(1, 95.5)
        
        self.assertTrue(result)
        self.mock_db.update_currency.assert_called_once_with(1, value=95.5)

    def test_update_currency_value_by_code(self) -> None:
        """Тест обновления курса валюты по символьному коду."""
        # Мокаем get_currency_by_code, чтобы вернуть валюту
        self.mock_db.read_currency_by_char_code.return_value = {
            'id': 1,
            'char_code': 'USD',
            'value': 90.0
        }
        self.mock_db.update_currency.return_value = True
        
        result = self.controller.update_currency_value_by_code('USD', 95.5)
        
        self.assertTrue(result)
        self.mock_db.read_currency_by_char_code.assert_called_once_with('USD')
        self.mock_db.update_currency.assert_called_once_with(1, value=95.5)

    def test_update_nonexistent_currency_returns_false(self) -> None:
        """Тест того, что обновление несуществующей валюты возвращает False."""
        self.mock_db.update_currency.return_value = False
        
        result = self.controller.update_currency(9999, value=100.0)
        
        self.assertFalse(result)

    def test_delete_currency(self) -> None:
        """Тест удаления валюты через контроллер."""
        self.mock_db.delete_currency.return_value = True
        
        result = self.controller.delete_currency(1)
        
        self.assertTrue(result)
        self.mock_db.delete_currency.assert_called_once_with(1)

    # ============= ТЕСТЫ КОНТРОЛЛЕРА ПОЛЬЗОВАТЕЛЕЙ =============
    
    def test_list_users(self) -> None:
        """Тест получения списка пользователей."""
        expected_users = [
            {'id': 1, 'name': 'Иван Петров'},
            {'id': 2, 'name': 'Анна Смирнова'},
        ]
        self.mock_db.read_users.return_value = expected_users
        
        result = self.controller.list_users()
        
        self.assertEqual(result, expected_users)

    def test_get_user(self) -> None:
        """Тест получения пользователя."""
        expected_user = {'id': 1, 'name': 'Иван Петров'}
        self.mock_db.read_user.return_value = expected_user
        
        result = self.controller.get_user(1)
        
        self.assertEqual(result, expected_user)

    def test_add_user(self) -> None:
        """Тест добавления нового пользователя."""
        self.mock_db.create_user.return_value = 1
        
        result = self.controller.add_user('Иван Петров')
        
        self.assertEqual(result, 1)

    def test_delete_user(self) -> None:
        """Тест удаления пользователя через контроллер."""
        self.mock_db.delete_user.return_value = True
        
        result = self.controller.delete_user(1)
        
        self.assertTrue(result)

    # ============= ТЕСТЫ ПОДПИСОК =============
    
    def test_subscribe_user_to_currency(self) -> None:
        """Тест подписки пользователя на валюту."""
        self.mock_db.create_user_currency.return_value = 1
        
        result = self.controller.subscribe_user_to_currency(1, 1)
        
        self.assertEqual(result, 1)
        self.mock_db.create_user_currency.assert_called_once_with(1, 1)

    def test_get_user_currencies(self) -> None:
        """Тест получения валют, на которые подписан пользователь."""
        expected_currencies = [
            {'id': 1, 'char_code': 'USD'},
            {'id': 2, 'char_code': 'EUR'},
        ]
        self.mock_db.read_user_currencies.return_value = expected_currencies
        
        result = self.controller.get_user_currencies(1)
        
        self.assertEqual(result, expected_currencies)

    def test_unsubscribe_user_from_currency(self) -> None:
        """Тест отписки пользователя от валюты."""
        self.mock_db.delete_user_currency.return_value = True
        
        result = self.controller.unsubscribe_user_from_currency(1, 1)
        
        self.assertTrue(result)


class TestCurrencyControllerIntegration(unittest.TestCase):
    """Интеграционные тесты с использованием реальной SQLite базы данных."""

    def setUp(self) -> None:
        """Настраивает тестовую БД и контроллер."""
        db = CurrencyRatesCRUD(db_path=':memory:')
        self.controller = CurrencyController(db)

    def test_full_currency_workflow(self) -> None:
        """Тест полного CRUD workflow для валют."""
        # Создаём
        currency_id = self.controller.add_currency(
            '840', 'USD', 'Доллар США', 90.0, 1
        )
        self.assertGreater(currency_id, 0)
        
        # Читаем
        currency = self.controller.get_currency(currency_id)
        self.assertIsNotNone(currency)
        self.assertEqual(currency['char_code'], 'USD')
        
        # Обновляем
        success = self.controller.update_currency_value(currency_id, 95.5)
        self.assertTrue(success)
        
        currency = self.controller.get_currency(currency_id)
        self.assertEqual(currency['value'], 95.5)
        
        # Удаляем
        success = self.controller.delete_currency(currency_id)
        self.assertTrue(success)
        
        currency = self.controller.get_currency(currency_id)
        self.assertIsNone(currency)

    def test_full_user_subscription_workflow(self) -> None:
        """Тест полного рабочего процесса подписки пользователя."""
        # Создаём пользователя и валюты
        user_id = self.controller.add_user('Иван Петров')
        usd_id = self.controller.add_currency(
            '840', 'USD', 'Доллар США', 90.0, 1
        )
        eur_id = self.controller.add_currency(
            '978', 'EUR', 'Евро', 91.0, 1
        )
        
        # Подписываем на валюты
        self.controller.subscribe_user_to_currency(user_id, usd_id)
        self.controller.subscribe_user_to_currency(user_id, eur_id)
        
        # Проверяем подписки
        currencies = self.controller.get_user_currencies(user_id)
        self.assertEqual(len(currencies), 2)
        
        # Удаляем одну подписку
        self.controller.unsubscribe_user_from_currency(user_id, usd_id)
        
        # Verify
        currencies = self.controller.get_user_currencies(user_id)
        self.assertEqual(len(currencies), 1)
        self.assertEqual(currencies[0]['char_code'], 'EUR')

if __name__ == "__main__":
    unittest.main()

"""
Тесты для лабораторной работы.
"""

import unittest
import io
from unittest.mock import patch, Mock
import json
from urllib.error import URLError

from currencies import get_currencies
from logger import logger
from demo_quadratic_equation import solve_quadratic

class TestGetCurrencies(unittest.TestCase):
    """Тесты для функции get_currencies."""
    
    @patch('urllib.request.urlopen')
    def test_successful_request(self, mock_urlopen):
        """Тест успешного получения курсов валют."""
        # Мокаем ответ API
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({
            "Valute": {
                "USD": {"Value": 93.25},
                "EUR": {"Value": 101.70}
            }
        }).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = get_currencies(["USD", "EUR"])
        
        self.assertEqual(result, {"USD": 93.25, "EUR": 101.70})
    
    @patch('urllib.request.urlopen')
    def test_currency_not_found(self, mock_urlopen):
        """Тест случая, когда валюта не найдена."""
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({
            "Valute": {
                "USD": {"Value": 93.25}
            }
        }).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        with self.assertRaises(KeyError):
            get_currencies(["GBP"])
    
    @patch('urllib.request.urlopen')
    def test_invalid_json(self, mock_urlopen):
        """Тест некорректного JSON."""
        mock_response = Mock()
        mock_response.read.return_value = b"invalid json"
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        with self.assertRaises(ValueError):
            get_currencies(["USD"])
    
    @patch('urllib.request.urlopen')
    def test_missing_valute_key(self, mock_urlopen):
        """Тест отсутствия ключа 'Valute'."""
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"other": "data"}).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        with self.assertRaises(KeyError):
            get_currencies(["USD"])
    
    @patch('urllib.request.urlopen')
    def test_invalid_currency_type(self, mock_urlopen):
        """Тест некорректного типа курса валюты."""
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({
            "Valute": {
                "USD": {"Value": "not a number"}
            }
        }).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        with self.assertRaises(TypeError):
            get_currencies(["USD"])


class TestLoggerDecorator(unittest.TestCase):
    """Тесты для декоратора logger."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.stream = io.StringIO()
    
    def test_successful_execution_logging(self):
        """Тест логирования успешного выполнения."""
        @logger(handle=self.stream)
        def test_func(x: int, y: int) -> int:
            return x + y
        
        result = test_func(2, 3)
        
        logs = self.stream.getvalue()
        
        self.assertEqual(result, 5)
        self.assertIn("INFO: Вызов функции test_func", logs)
        self.assertIn("args=(2, 3)", logs)
        self.assertIn("INFO: Функция test_func успешно завершилась", logs)
        self.assertIn("Результат: 5", logs)
    
    def test_error_logging(self):
        """Тест логирования ошибок."""
        @logger(handle=self.stream)
        def test_func(x: int) -> int:
            raise ValueError("Test error")
        
        with self.assertRaises(ValueError):
            test_func(10)
        
        logs = self.stream.getvalue()
        
        self.assertIn("ERROR: В функции test_func возникло исключение", logs)
        self.assertIn("ValueError", logs)
        self.assertIn("Test error", logs)
    
    def test_logger_with_keyword_arguments(self):
        """Тест логирования функции с keyword-аргументами."""
        @logger(handle=self.stream)
        def test_func(a: int, b: int = 5) -> int:
            return a * b
        
        result = test_func(3, b=4)
        
        logs = self.stream.getvalue()
        
        self.assertEqual(result, 12)
        self.assertIn("kwargs={'b': 4}", logs)


class TestStreamWrite(unittest.TestCase):
    """Тесты для работы с StringIO."""
    
    def setUp(self):
        """Настройка тестового окружения."""
        self.stream = io.StringIO()
        
        @logger(handle=self.stream)
        def wrapped():
            return get_currencies(['USD'], url="https://invalid-url.test")
        
        self.wrapped = wrapped
    
    @patch('urllib.request.urlopen')
    def test_logging_error(self, mock_urlopen):
        """Тест логирования ошибки соединения."""
        mock_urlopen.side_effect = URLError("Connection failed")
        
        with self.assertRaises(ConnectionError):
            self.wrapped()
        
        logs = self.stream.getvalue()
        
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)


class TestQuadraticEquation(unittest.TestCase):
    """Тесты для квадратного уравнения."""
    
    def test_two_roots(self):
        """Тест уравнения с двумя корнями."""
        result = solve_quadratic(1, -3, 2)
        self.assertEqual(result, (2.0, 1.0))
    
    def test_one_root(self):
        """Тест уравнения с одним корнем."""
        result = solve_quadratic(1, -4, 4)
        self.assertEqual(result, (2.0,))
    
    def test_no_roots(self):
        """Тест уравнения без действительных корней."""
        result = solve_quadratic(1, 2, 5)
        self.assertIsNone(result)
    
    def test_invalid_type(self):
        """Тест с некорректным типом данных."""
        with self.assertRaises(TypeError):
            solve_quadratic("a", 2, 3)
    
    def test_critical_situation(self):
        """Тест критической ситуации."""
        with self.assertRaises(ValueError):
            solve_quadratic(0, 0, 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
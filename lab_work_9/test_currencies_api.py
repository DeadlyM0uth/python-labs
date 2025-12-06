"""Тесты для функции получения курсов валют.

Содержит юнит-тесты для функций get_currencies и get_currencies_by_code.
"""

import unittest
from unittest.mock import patch, MagicMock
import urllib.error
import xml.etree.ElementTree as ET

from myapp.utils import get_currencies, get_currencies_by_code


class TestGetCurrencies(unittest.TestCase):
    """Тесты для функции get_currencies."""

    def setUp(self) -> None:
        """Подготовка к каждому тесту."""
        # Примеры XML ответов для тестирования
        self.valid_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <ValCurs Date="01.12.2024" name="Курсы">
            <Valute ID="R01235">
                <NumCode>840</NumCode>
                <CharCode>USD</CharCode>
                <Nominal>1</Nominal>
                <Name>Доллар США</Name>
                <Value>75.5</Value>
            </Valute>
            <Valute ID="R01239">
                <NumCode>978</NumCode>
                <CharCode>EUR</CharCode>
                <Nominal>1</Nominal>
                <Name>Евро</Name>
                <Value>82.3</Value>
            </Valute>
        </ValCurs>
        """

        self.empty_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <ValCurs Date="01.12.2024" name="Курсы">
        </ValCurs>
        """

        self.invalid_xml = "This is not valid XML"

    @patch('urllib.request.urlopen')
    def test_get_currencies_success(self, mock_urlopen) -> None:
        """Тест успешного получения курсов валют."""
        # Подготавливаем mock
        mock_response = MagicMock()
        mock_response.read.return_value = self.valid_xml.encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = False
        mock_urlopen.return_value = mock_response

        # Вызываем функцию
        currencies = get_currencies()

        # Проверяем результат
        self.assertEqual(len(currencies), 2)
        self.assertEqual(currencies[0]['char_code'], 'USD')
        self.assertEqual(currencies[0]['value'], '75.5')
        self.assertEqual(currencies[1]['char_code'], 'EUR')

    @patch('urllib.request.urlopen')
    def test_get_currencies_url_error(self, mock_urlopen) -> None:
        """Тест обработки ошибки подключения."""
        # Подготавливаем mock для ошибки подключения
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

        # Проверяем, что исключение выбрасывается
        with self.assertRaises(urllib.error.URLError):
            get_currencies()

    @patch('urllib.request.urlopen')
    def test_get_currencies_invalid_xml(self, mock_urlopen) -> None:
        """Тест обработки невалидного XML."""
        # Подготавливаем mock с невалидным XML
        mock_response = MagicMock()
        mock_response.read.return_value = self.invalid_xml.encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = False
        mock_urlopen.return_value = mock_response

        # Проверяем, что исключение выбрасывается
        with self.assertRaises(ET.ParseError):
            get_currencies()

    @patch('urllib.request.urlopen')
    def test_get_currencies_empty_xml(self, mock_urlopen) -> None:
        """Тест обработки пустого XML (без валют)."""
        # Подготавливаем mock с пустым XML
        mock_response = MagicMock()
        mock_response.read.return_value = self.empty_xml.encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = False
        mock_urlopen.return_value = mock_response

        # Проверяем, что исключение выбрасывается
        with self.assertRaises(ValueError):
            get_currencies()

    @patch('urllib.request.urlopen')
    def test_get_currencies_correct_fields(self, mock_urlopen) -> None:
        """Тест проверки всех полей в результате."""
        # Подготавливаем mock
        mock_response = MagicMock()
        mock_response.read.return_value = self.valid_xml.encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = False
        mock_urlopen.return_value = mock_response

        # Вызываем функцию
        currencies = get_currencies()

        # Проверяем, что все необходимые поля присутствуют
        required_fields = ['id', 'num_code', 'char_code', 'name', 'value', 'nominal']
        for currency in currencies:
            for field in required_fields:
                self.assertIn(field, currency)


class TestGetCurrenciesByCode(unittest.TestCase):
    """Тесты для функции get_currencies_by_code."""

    def setUp(self) -> None:
        """Подготовка к каждому тесту."""
        self.currencies = [
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

    def test_get_currencies_by_code_found(self) -> None:
        """Тест поиска валюты по символьному коду (валюта найдена)."""
        currency = get_currencies_by_code('USD', self.currencies)
        self.assertIsNotNone(currency)
        self.assertEqual(currency['char_code'], 'USD')
        self.assertEqual(currency['name'], 'Доллар США')

    def test_get_currencies_by_code_case_insensitive(self) -> None:
        """Тест что поиск не зависит от регистра."""
        currency = get_currencies_by_code('usd', self.currencies)
        self.assertIsNotNone(currency)
        self.assertEqual(currency['char_code'], 'USD')

    def test_get_currencies_by_code_not_found(self) -> None:
        """Тест поиска валюты по символьному коду (валюта не найдена)."""
        currency = get_currencies_by_code('GBP', self.currencies)
        self.assertIsNone(currency)

    def test_get_currencies_by_code_eur(self) -> None:
        """Тест поиска евро."""
        currency = get_currencies_by_code('EUR', self.currencies)
        self.assertIsNotNone(currency)
        self.assertEqual(currency['char_code'], 'EUR')

    @patch('myapp.utils.currencies_api.get_currencies')
    def test_get_currencies_by_code_without_list(self, mock_get_currencies) -> None:
        """Тест получения валюты по коду без передачи списка."""
        mock_get_currencies.return_value = self.currencies

        currency = get_currencies_by_code('USD')
        self.assertIsNotNone(currency)
        self.assertEqual(currency['char_code'], 'USD')

    @patch('myapp.utils.currencies_api.get_currencies')
    def test_get_currencies_by_code_api_error(self, mock_get_currencies) -> None:
        """Тест обработки ошибки при получении валют."""
        mock_get_currencies.side_effect = urllib.error.URLError("Connection error")

        with self.assertRaises(urllib.error.URLError):
            get_currencies_by_code('USD')


if __name__ == "__main__":
    unittest.main()

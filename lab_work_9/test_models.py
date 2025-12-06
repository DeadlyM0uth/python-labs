"""Тесты для моделей приложения.

Содержит юнит-тесты для всех моделей с проверкой геттеров,
сеттеров и валидации данных.
"""

import unittest
from myapp.models import Author, App, User, Currency, UserCurrency


class TestAuthor(unittest.TestCase):
    """Тесты для класса Author."""

    def setUp(self) -> None:
        """Подготовка к каждому тесту."""
        self.author = Author(name="Иван Иванов", group="P3120")

    def test_author_creation(self) -> None:
        """Тест создания объекта Author."""
        self.assertEqual(self.author.name, "Иван Иванов")
        self.assertEqual(self.author.group, "P3120")

    def test_author_name_setter(self) -> None:
        """Тест установки имени автора."""
        self.author.name = "Петр Петров"
        self.assertEqual(self.author.name, "Петр Петров")

    def test_author_name_setter_with_spaces(self) -> None:
        """Тест установки имени с лишними пробелами."""
        self.author.name = "  Сергей Сергеев  "
        self.assertEqual(self.author.name, "Сергей Сергеев")

    def test_author_name_invalid_type(self) -> None:
        """Тест установки имени с неверным типом."""
        with self.assertRaises(TypeError):
            self.author.name = 123

    def test_author_name_empty(self) -> None:
        """Тест установки пустого имени."""
        with self.assertRaises(ValueError):
            self.author.name = ""

    def test_author_group_setter(self) -> None:
        """Тест установки группы."""
        self.author.group = "P3121"
        self.assertEqual(self.author.group, "P3121")

    def test_author_group_invalid_type(self) -> None:
        """Тест установки группы с неверным типом."""
        with self.assertRaises(TypeError):
            self.author.group = 123

    def test_author_group_empty(self) -> None:
        """Тест установки пустой группы."""
        with self.assertRaises(ValueError):
            self.author.group = ""

    def test_author_repr(self) -> None:
        """Тест строкового представления для отладки."""
        repr_str = repr(self.author)
        self.assertIn("Иван Иванов", repr_str)
        self.assertIn("P3120", repr_str)

    def test_author_str(self) -> None:
        """Тест пользовательского строкового представления."""
        str_repr = str(self.author)
        self.assertEqual(str_repr, "Иван Иванов (P3120)")


class TestApp(unittest.TestCase):
    """Тесты для класса App."""

    def setUp(self) -> None:
        """Подготовка к каждому тесту."""
        self.author = Author(name="Иван Иванов", group="P3120")
        self.app = App(name="MyApp", version="1.0.0", author=self.author)

    def test_app_creation(self) -> None:
        """Тест создания объекта App."""
        self.assertEqual(self.app.name, "MyApp")
        self.assertEqual(self.app.version, "1.0.0")
        self.assertEqual(self.app.author.name, "Иван Иванов")

    def test_app_name_setter(self) -> None:
        """Тест установки названия приложения."""
        self.app.name = "NewApp"
        self.assertEqual(self.app.name, "NewApp")

    def test_app_name_invalid_type(self) -> None:
        """Тест установки названия с неверным типом."""
        with self.assertRaises(TypeError):
            self.app.name = 123

    def test_app_name_empty(self) -> None:
        """Тест установки пустого названия."""
        with self.assertRaises(ValueError):
            self.app.name = ""

    def test_app_version_valid_formats(self) -> None:
        """Тест установки версии в различных форматах."""
        valid_versions = ["1.0.0", "2.5.10", "0.0.1", "999.999.999"]
        for version in valid_versions:
            self.app.version = version
            self.assertEqual(self.app.version, version)

    def test_app_version_invalid_format(self) -> None:
        """Тест установки версии с неверным форматом."""
        invalid_versions = ["1.0", "1.0.0.0", "1.a.0", "abc"]
        for version in invalid_versions:
            with self.assertRaises(ValueError):
                self.app.version = version

    def test_app_version_invalid_type(self) -> None:
        """Тест установки версии с неверным типом."""
        with self.assertRaises(TypeError):
            self.app.version = 1.0

    def test_app_author_setter(self) -> None:
        """Тест установки автора."""
        new_author = Author(name="Петр Петров", group="P3121")
        self.app.author = new_author
        self.assertEqual(self.app.author.name, "Петр Петров")

    def test_app_author_invalid_type(self) -> None:
        """Тест установки автора с неверным типом."""
        with self.assertRaises(TypeError):
            self.app.author = "Not an author"

    def test_app_str(self) -> None:
        """Тест пользовательского строкового представления."""
        str_repr = str(self.app)
        self.assertIn("MyApp", str_repr)
        self.assertIn("1.0.0", str_repr)


class TestUser(unittest.TestCase):
    """Тесты для класса User."""

    def setUp(self) -> None:
        """Подготовка к каждому тесту."""
        self.user = User(user_id=1, name="Иван Иванов")

    def test_user_creation(self) -> None:
        """Тест создания объекта User."""
        self.assertEqual(self.user.id, 1)
        self.assertEqual(self.user.name, "Иван Иванов")

    def test_user_id_setter(self) -> None:
        """Тест установки ID пользователя."""
        self.user.id = 5
        self.assertEqual(self.user.id, 5)

    def test_user_id_invalid_type(self) -> None:
        """Тест установки ID с неверным типом."""
        with self.assertRaises(TypeError):
            self.user.id = "not_an_int"

    def test_user_id_zero(self) -> None:
        """Тест установки нулевого ID."""
        with self.assertRaises(ValueError):
            self.user.id = 0

    def test_user_id_negative(self) -> None:
        """Тест установки отрицательного ID."""
        with self.assertRaises(ValueError):
            self.user.id = -1

    def test_user_name_setter(self) -> None:
        """Тест установки имени пользователя."""
        self.user.name = "Петр Петров"
        self.assertEqual(self.user.name, "Петр Петров")

    def test_user_name_invalid_type(self) -> None:
        """Тест установки имени с неверным типом."""
        with self.assertRaises(TypeError):
            self.user.name = 123

    def test_user_name_empty(self) -> None:
        """Тест установки пустого имени."""
        with self.assertRaises(ValueError):
            self.user.name = ""

    def test_user_equality(self) -> None:
        """Тест сравнения пользователей по ID."""
        user2 = User(user_id=1, name="Другое имя")
        self.assertEqual(self.user, user2)

    def test_user_hash(self) -> None:
        """Тест хеширования пользователя."""
        user2 = User(user_id=1, name="Другое имя")
        self.assertEqual(hash(self.user), hash(user2))


class TestCurrency(unittest.TestCase):
    """Тесты для класса Currency."""

    def setUp(self) -> None:
        """Подготовка к каждому тесту."""
        self.currency = Currency(
            currency_id="R01235",
            num_code="840",
            char_code="USD",
            name="Доллар США",
            value="75.5",
            nominal="1",
        )

    def test_currency_creation(self) -> None:
        """Тест создания объекта Currency."""
        self.assertEqual(self.currency.id, "R01235")
        self.assertEqual(self.currency.num_code, "840")
        self.assertEqual(self.currency.char_code, "USD")
        self.assertEqual(self.currency.value, 75.5)
        self.assertEqual(self.currency.nominal, 1)

    def test_currency_char_code_uppercase(self) -> None:
        """Тест преобразования символьного кода в верхний регистр."""
        currency = Currency(
            currency_id="R01235",
            num_code="840",
            char_code="usd",
            name="Доллар США",
            value="75.5",
            nominal="1",
        )
        self.assertEqual(currency.char_code, "USD")

    def test_currency_num_code_invalid(self) -> None:
        """Тест установки неверного цифрового кода."""
        with self.assertRaises(ValueError):
            self.currency.num_code = "84"  # Только 2 цифры
        with self.assertRaises(ValueError):
            self.currency.num_code = "abc"  # Не цифры

    def test_currency_char_code_invalid(self) -> None:
        """Тест установки неверного символьного кода."""
        with self.assertRaises(ValueError):
            self.currency.char_code = "US"  # Только 2 буквы
        with self.assertRaises(ValueError):
            self.currency.char_code = "123"  # Цифры, а не буквы

    def test_currency_value_with_comma(self) -> None:
        """Тест установки значения курса с запятой."""
        self.currency.value = "75,5"
        self.assertEqual(self.currency.value, 75.5)

    def test_currency_value_invalid(self) -> None:
        """Тест установки неверного значения курса."""
        with self.assertRaises(ValueError):
            self.currency.value = "not_a_number"

    def test_currency_value_negative(self) -> None:
        """Тест установки отрицательного значения курса."""
        with self.assertRaises(ValueError):
            self.currency.value = "-75.5"

    def test_currency_nominal_invalid(self) -> None:
        """Тест установки неверного номинала."""
        with self.assertRaises(ValueError):
            self.currency.nominal = "0"
        with self.assertRaises(ValueError):
            self.currency.nominal = "-1"

    def test_currency_equality(self) -> None:
        """Тест сравнения валют по ID."""
        currency2 = Currency(
            currency_id="R01235",
            num_code="999",
            char_code="XXX",
            name="Другое название",
            value="999.9",
            nominal="999",
        )
        self.assertEqual(self.currency, currency2)

    def test_currency_hash(self) -> None:
        """Тест хеширования валюты."""
        currency2 = Currency(
            currency_id="R01235",
            num_code="999",
            char_code="XXX",
            name="Другое название",
            value="999.9",
            nominal="999",
        )
        self.assertEqual(hash(self.currency), hash(currency2))


class TestUserCurrency(unittest.TestCase):
    """Тесты для класса UserCurrency."""

    def setUp(self) -> None:
        """Подготовка к каждому тесту."""
        self.user_currency = UserCurrency(
            uc_id=1,
            user_id=1,
            currency_id="R01235",
        )

    def test_user_currency_creation(self) -> None:
        """Тест создания объекта UserCurrency."""
        self.assertEqual(self.user_currency.id, 1)
        self.assertEqual(self.user_currency.user_id, 1)
        self.assertEqual(self.user_currency.currency_id, "R01235")

    def test_user_currency_id_setter(self) -> None:
        """Тест установки ID записи."""
        self.user_currency.id = 5
        self.assertEqual(self.user_currency.id, 5)

    def test_user_currency_id_invalid(self) -> None:
        """Тест установки неверного ID записи."""
        with self.assertRaises(ValueError):
            self.user_currency.id = 0
        with self.assertRaises(ValueError):
            self.user_currency.id = -1

    def test_user_currency_user_id_setter(self) -> None:
        """Тест установки user_id."""
        self.user_currency.user_id = 2
        self.assertEqual(self.user_currency.user_id, 2)

    def test_user_currency_user_id_invalid(self) -> None:
        """Тест установки неверного user_id."""
        with self.assertRaises(ValueError):
            self.user_currency.user_id = 0
        with self.assertRaises(ValueError):
            self.user_currency.user_id = -1

    def test_user_currency_currency_id_setter(self) -> None:
        """Тест установки currency_id."""
        self.user_currency.currency_id = "R01239"
        self.assertEqual(self.user_currency.currency_id, "R01239")

    def test_user_currency_currency_id_invalid(self) -> None:
        """Тест установки пустого currency_id."""
        with self.assertRaises(ValueError):
            self.user_currency.currency_id = ""

    def test_user_currency_equality(self) -> None:
        """Тест сравнения подписок по user_id и currency_id."""
        uc2 = UserCurrency(uc_id=999, user_id=1, currency_id="R01235")
        self.assertEqual(self.user_currency, uc2)

    def test_user_currency_hash(self) -> None:
        """Тест хеширования подписки."""
        uc2 = UserCurrency(uc_id=999, user_id=1, currency_id="R01235")
        self.assertEqual(hash(self.user_currency), hash(uc2))


if __name__ == "__main__":
    unittest.main()

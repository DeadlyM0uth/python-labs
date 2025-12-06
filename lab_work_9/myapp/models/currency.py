"""Модель валюты.

Содержит информацию о валюте, включая коды, название и текущий курс.
"""

from typing import Union


class Currency:
    """Класс, представляющий валюту.
    
    Атрибуты:
        _id: Уникальный идентификатор валюты (приватный атрибут).
        _num_code: Цифровой код валюты (приватный атрибут).
        _char_code: Символьный код валюты (приватный атрибут).
        _name: Название валюты (приватный атрибут).
        _value: Курс валюты (приватный атрибут).
        _nominal: Номинал валюты (приватный атрибут).
    """

    def __init__(
        self,
        currency_id: str,
        num_code: str,
        char_code: str,
        name: str,
        value: str,
        nominal: str,
    ) -> None:
        """Инициализирует объект Currency.
        
        Args:
            currency_id: Уникальный идентификатор валюты.
            num_code: Цифровой код валюты (3 цифры).
            char_code: Символьный код валюты (3 буквы).
            name: Название валюты.
            value: Курс валюты (строка с запятой как разделитель).
            nominal: Номинал валюты (за сколько единиц указан курс).
            
        Raises:
            TypeError: Если параметры имеют неверные типы.
            ValueError: Если параметры пусты или имеют неверный формат.
        """
        self.id = currency_id
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def id(self) -> str:
        """Получает идентификатор валюты.
        
        Returns:
            Уникальный идентификатор валюты.
        """
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        """Устанавливает идентификатор валюты.
        
        Args:
            value: Новый идентификатор валюты.
            
        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value пустая строка.
        """
        if not isinstance(value, str):
            raise TypeError(f"ID должен быть строкой, получено: {type(value).__name__}")
        if not value.strip():
            raise ValueError("ID не может быть пустым")
        self._id = value.strip()

    @property
    def num_code(self) -> str:
        """Получает цифровой код валюты.
        
        Returns:
            Цифровой код валюты.
        """
        return self._num_code

    @num_code.setter
    def num_code(self, value: str) -> None:
        """Устанавливает цифровой код валюты.
        
        Args:
            value: Новый цифровой код (3 цифры).
            
        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value не равен 3 цифрам.
        """
        if not isinstance(value, str):
            raise TypeError(f"Цифровой код должен быть строкой, получено: {type(value).__name__}")
        if not value.isdigit() or len(value) != 3:
            raise ValueError(f"Цифровой код должен состоять из 3 цифр, получено: {value}")
        self._num_code = value

    @property
    def char_code(self) -> str:
        """Получает символьный код валюты.
        
        Returns:
            Символьный код валюты.
        """
        return self._char_code

    @char_code.setter
    def char_code(self, value: str) -> None:
        """Устанавливает символьный код валюты.
        
        Args:
            value: Новый символьный код (3 буквы).
            
        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value не равен 3 буквам.
        """
        if not isinstance(value, str):
            raise TypeError(f"Символьный код должен быть строкой, получено: {type(value).__name__}")
        value_upper = value.upper()
        if not value_upper.isalpha() or len(value_upper) != 3:
            raise ValueError(f"Символьный код должен состоять из 3 букв, получено: {value}")
        self._char_code = value_upper

    @property
    def name(self) -> str:
        """Получает название валюты.
        
        Returns:
            Название валюты.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Устанавливает название валюты.
        
        Args:
            value: Новое название валюты.
            
        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value пустая строка.
        """
        if not isinstance(value, str):
            raise TypeError(f"Название должно быть строкой, получено: {type(value).__name__}")
        if not value.strip():
            raise ValueError("Название не может быть пустым")
        self._name = value.strip()

    @property
    def value(self) -> float:
        """Получает курс валюты.
        
        Returns:
            Курс валюты в виде float.
        """
        return self._value

    @value.setter
    def value(self, value: Union[str, float, int]) -> None:
        """Устанавливает курс валюты.
        
        Args:
            value: Новый курс валюты (строка или число).
                  Строка может содержать запятую как разделитель.
            
        Raises:
            TypeError: Если value имеет неверный тип.
            ValueError: Если value не может быть преобразован в float.
        """
        if isinstance(value, str):
            # Заменяем запятую на точку для корректного преобразования
            value = value.strip().replace(',', '.')
        
        try:
            float_value = float(value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Курс должен быть числом, получено: {value}") from e
        
        if float_value < 0:
            raise ValueError(f"Курс не может быть отрицательным, получено: {float_value}")
        
        self._value = float_value

    @property
    def nominal(self) -> int:
        """Получает номинал валюты.
        
        Returns:
            Номинал валюты (за сколько единиц указан курс).
        """
        return self._nominal

    @nominal.setter
    def nominal(self, value: Union[str, int]) -> None:
        """Устанавливает номинал валюты.
        
        Args:
            value: Новый номинал валюты.
            
        Raises:
            TypeError: Если value имеет неверный тип.
            ValueError: Если value не положительное целое число.
        """
        if isinstance(value, str):
            value = value.strip()
        
        try:
            int_value = int(value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Номинал должен быть целым числом, получено: {value}") from e
        
        if int_value <= 0:
            raise ValueError(f"Номинал должен быть положительным числом, получено: {int_value}")
        
        self._nominal = int_value

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта для отладки.
        
        Returns:
            Строка с информацией о валюте.
        """
        return (
            f"Currency(id={self._id!r}, num_code={self._num_code!r}, "
            f"char_code={self._char_code!r}, name={self._name!r}, "
            f"value={self._value}, nominal={self._nominal})"
        )

    def __str__(self) -> str:
        """Возвращает пользовательское строковое представление.
        
        Returns:
            Форматированная строка с данными валюты.
        """
        return f"{self._char_code} - {self._name}: {self._value:.4f} за {self._nominal}"

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство двух валют по ID.
        
        Args:
            other: Другой объект для сравнения.
            
        Returns:
            True, если валюты имеют одинаковый ID, False иначе.
        """
        if not isinstance(other, Currency):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        """Возвращает хэш валюты для использования в хэш-таблицах.
        
        Returns:
            Хэш ID валюты.
        """
        return hash(self._id)

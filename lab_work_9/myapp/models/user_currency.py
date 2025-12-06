"""Модель связи пользователя и валюты.

Реализует отношение "много ко многим" между пользователями и валютами.
Описывает подписку пользователя на определённую валюту.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myapp.models.user import User
    from myapp.models.currency import Currency


class UserCurrency:
    """Класс, представляющий подписку пользователя на валюту.
    
    Реализует связь "много ко многим" между User и Currency.
    
    Атрибуты:
        _id: Уникальный идентификатор записи (приватный атрибут).
        _user_id: ID пользователя (внешний ключ) (приватный атрибут).
        _currency_id: ID валюты (внешний ключ) (приватный атрибут).
    """

    def __init__(self, uc_id: int, user_id: int, currency_id: str) -> None:
        """Инициализирует объект UserCurrency.
        
        Args:
            uc_id: Уникальный идентификатор записи UserCurrency.
            user_id: ID пользователя (внешний ключ к User).
            currency_id: ID валюты (внешний ключ к Currency).
            
        Raises:
            TypeError: Если параметры имеют неверные типы.
            ValueError: Если user_id отрицательный.
        """
        self.id = uc_id
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self) -> int:
        """Получает идентификатор записи.
        
        Returns:
            Уникальный идентификатор записи UserCurrency.
        """
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        """Устанавливает идентификатор записи.
        
        Args:
            value: Новый идентификатор.
            
        Raises:
            TypeError: Если value не является целым числом.
            ValueError: Если value отрицательный или нулевой.
        """
        if not isinstance(value, int):
            raise TypeError(f"ID должен быть целым числом, получено: {type(value).__name__}")
        if value <= 0:
            raise ValueError(f"ID должен быть положительным числом, получено: {value}")
        self._id = value

    @property
    def user_id(self) -> int:
        """Получает ID пользователя.
        
        Returns:
            ID пользователя (внешний ключ).
        """
        return self._user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        """Устанавливает ID пользователя.
        
        Args:
            value: Новый ID пользователя.
            
        Raises:
            TypeError: Если value не является целым числом.
            ValueError: Если value отрицательный или нулевой.
        """
        if not isinstance(value, int):
            raise TypeError(f"user_id должен быть целым числом, получено: {type(value).__name__}")
        if value <= 0:
            raise ValueError(f"user_id должен быть положительным числом, получено: {value}")
        self._user_id = value

    @property
    def currency_id(self) -> str:
        """Получает ID валюты.
        
        Returns:
            ID валюты (внешний ключ).
        """
        return self._currency_id

    @currency_id.setter
    def currency_id(self, value: str) -> None:
        """Устанавливает ID валюты.
        
        Args:
            value: Новый ID валюты.
            
        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value пустая строка.
        """
        if not isinstance(value, str):
            raise TypeError(f"currency_id должен быть строкой, получено: {type(value).__name__}")
        if not value.strip():
            raise ValueError("currency_id не может быть пустым")
        self._currency_id = value.strip()

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта для отладки.
        
        Returns:
            Строка с информацией о подписке.
        """
        return f"UserCurrency(id={self._id}, user_id={self._user_id}, currency_id={self._currency_id!r})"

    def __str__(self) -> str:
        """Возвращает пользовательское строковое представление.
        
        Returns:
            Форматированная строка с данными подписки.
        """
        return f"Пользователь {self._user_id} подписан на валюту {self._currency_id}"

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство двух записей подписки.
        
        Args:
            other: Другой объект для сравнения.
            
        Returns:
            True, если записи имеют одинаковые user_id и currency_id, False иначе.
        """
        if not isinstance(other, UserCurrency):
            return NotImplemented
        return self._user_id == other._user_id and self._currency_id == other._currency_id

    def __hash__(self) -> int:
        """Возвращает хэш подписки для использования в хэш-таблицах.
        
        Returns:
            Хэш кортежа (user_id, currency_id).
        """
        return hash((self._user_id, self._currency_id))

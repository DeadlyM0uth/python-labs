"""Модель пользователя.

Содержит информацию о пользователе приложения.
"""


class User:
    """Класс, представляющий пользователя приложения.
    
    Атрибуты:
        _id: Уникальный идентификатор пользователя (приватный атрибут).
        _name: Имя пользователя (приватный атрибут).
    """

    def __init__(self, user_id: int, name: str) -> None:
        """Инициализирует объект User.
        
        Args:
            user_id: Уникальный идентификатор пользователя.
            name: Имя пользователя.
            
        Raises:
            TypeError: Если параметры имеют неверные типы.
            ValueError: Если user_id отрицательный или name пустой.
        """
        self.id = user_id
        self.name = name

    @property
    def id(self) -> int:
        """Получает идентификатор пользователя.
        
        Returns:
            Уникальный идентификатор пользователя.
        """
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        """Устанавливает идентификатор пользователя.
        
        Args:
            value: Новый идентификатор пользователя.
            
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
    def name(self) -> str:
        """Получает имя пользователя.
        
        Returns:
            Имя пользователя.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Устанавливает имя пользователя.
        
        Args:
            value: Новое имя пользователя.
            
        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value пустая строка.
        """
        if not isinstance(value, str):
            raise TypeError(f"Имя должно быть строкой, получено: {type(value).__name__}")
        if not value.strip():
            raise ValueError("Имя не может быть пустым")
        self._name = value.strip()

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта для отладки.
        
        Returns:
            Строка с информацией о пользователе.
        """
        return f"User(id={self._id}, name={self._name!r})"

    def __str__(self) -> str:
        """Возвращает пользовательское строковое представление.
        
        Returns:
            Форматированная строка с данными пользователя.
        """
        return f"{self._name} (ID: {self._id})"

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство двух пользователей по ID.
        
        Args:
            other: Другой объект для сравнения.
            
        Returns:
            True, если пользователи имеют одинаковый ID, False иначе.
        """
        if not isinstance(other, User):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        """Возвращает хэш пользователя для использования в хэш-таблицах.
        
        Returns:
            Хэш ID пользователя.
        """
        return hash(self._id)

"""Модель приложения.

Содержит метаинформацию о приложении: название, версию и автора.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myapp.models.author import Author


class App:
    """Класс, представляющий приложение.
    
    Атрибуты:
        _name: Название приложения (приватный атрибут).
        _version: Версия приложения (приватный атрибут).
        _author: Объект Author (приватный атрибут).
    """

    def __init__(self, name: str, version: str, author: "Author") -> None:
        """Инициализирует объект App.
        
        Args:
            name: Название приложения.
            version: Версия приложения.
            author: Объект Author.
            
        Raises:
            TypeError: Если параметры имеют неверные типы.
            ValueError: Если name или version пусты.
        """
        self.name = name
        self.version = version
        self.author = author

    @property
    def name(self) -> str:
        """Получает название приложения.
        
        Returns:
            Название приложения.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Устанавливает название приложения.
        
        Args:
            value: Новое название приложения.
            
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
    def version(self) -> str:
        """Получает версию приложения.
        
        Returns:
            Версия приложения в формате X.Y.Z.
        """
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        """Устанавливает версию приложения.
        
        Args:
            value: Новая версия приложения.
            
        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value пустая или имеет неверный формат.
        """
        if not isinstance(value, str):
            raise TypeError(f"Версия должна быть строкой, получено: {type(value).__name__}")
        if not value.strip():
            raise ValueError("Версия не может быть пустой")
        
        # Проверка формата версии X.Y.Z
        parts = value.strip().split('.')
        if len(parts) != 3 or not all(part.isdigit() for part in parts):
            raise ValueError(f"Версия должна иметь формат X.Y.Z, получено: {value}")
        
        self._version = value.strip()

    @property
    def author(self) -> "Author":
        """Получает автора приложения.
        
        Returns:
            Объект Author.
        """
        return self._author

    @author.setter
    def author(self, value: "Author") -> None:
        """Устанавливает автора приложения.
        
        Args:
            value: Объект Author.
            
        Raises:
            TypeError: Если value не является объектом Author.
        """
        # Импортируем здесь для избежания циклической зависимости
        from myapp.models.author import Author
        
        if not isinstance(value, Author):
            raise TypeError(f"Автор должен быть объектом Author, получено: {type(value).__name__}")
        self._author = value

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта для отладки.
        
        Returns:
            Строка с информацией о приложении.
        """
        return f"App(name={self._name!r}, version={self._version!r}, author={self._author!r})"

    def __str__(self) -> str:
        """Возвращает пользовательское строковое представление.
        
        Returns:
            Форматированная строка с данными приложения.
        """
        return f"{self._name} v{self._version} by {self._author}"

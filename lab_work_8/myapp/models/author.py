"""Модель автора приложения.

Содержит информацию об авторе включая имя и учебную группу.
"""


class Author:
    """Класс, представляющий автора приложения.
    
    Атрибуты:
        _name: Имя автора (приватный атрибут).
        _group: Учебная группа автора (приватный атрибут).
    """

    def __init__(self, name: str, group: str) -> None:
        """Инициализирует объект Author.
        
        Args:
            name: Имя автора.
            group: Учебная группа автора.
            
        Raises:
            TypeError: Если name или group не являются строками.
            ValueError: Если name или group пусты.
        """
        self.name = name
        self.group = group

    @property
    def name(self) -> str:
        """Получает имя автора.
        
        Returns:
            Имя автора.
        """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Устанавливает имя автора с проверкой типа и корректности.
        
        Args:
            value: Новое имя автора.
            
        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value пустая строка.
        """
        if not isinstance(value, str):
            raise TypeError(f"Имя должно быть строкой, получено: {type(value).__name__}")
        if not value.strip():
            raise ValueError("Имя не может быть пустым")
        self._name = value.strip()

    @property
    def group(self) -> str:
        """Получает учебную группу автора.
        
        Returns:
            Учебная группа автора.
        """
        return self._group

    @group.setter
    def group(self, value: str) -> None:
        """Устанавливает учебную группу с проверкой типа и корректности.
        
        Args:
            value: Новая учебная группа.
            
        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value пустая строка.
        """
        if not isinstance(value, str):
            raise TypeError(f"Группа должна быть строкой, получено: {type(value).__name__}")
        if not value.strip():
            raise ValueError("Группа не может быть пустой")
        self._group = value.strip()

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта для отладки.
        
        Returns:
            Строка с информацией об авторе.
        """
        return f"Author(name={self._name!r}, group={self._group!r})"

    def __str__(self) -> str:
        """Возвращает пользовательское строковое представление.
        
        Returns:
            Форматированная строка с данными автора.
        """
        return f"{self._name} ({self._group})"

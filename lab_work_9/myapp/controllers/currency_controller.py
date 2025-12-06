"""Контроллер бизнес-логики для операций с валютами.

Реализует слой бизнес-логики в архитектуре MVC.
Обрабатывает высокоуровневые операции с валютами и управляет взаимодействием
между контроллером базы данных и рендерером представлений.
"""

from typing import List, Dict, Any, Optional
from myapp.controllers.database_controller import CurrencyRatesCRUD


class CurrencyController:
    """Контроллер бизнес-логики для управления валютами.
    
    Предоставляет высокоуровневые операции для управления валютами.
    Отделяет бизнес-логику от операций с базой данных и рендеринга представлений.
    
    Attributes:
        db: Экземпляр контроллера базы данных для CRUD операций.
    """

    def __init__(self, db_controller: CurrencyRatesCRUD) -> None:
        """Инициализирует контроллер валют.
        
        Args:
            db_controller: Экземпляр CurrencyRatesCRUD для операций с базой данных.
        """
        self.db: CurrencyRatesCRUD = db_controller

    def list_currencies(self) -> List[Dict[str, Any]]:
        """Получает все валюты из базы данных.
        
        Returns:
            Список словарей валют с ключами: id, num_code, char_code,
            name, value, nominal.
        
        Raises:
            Exception: Если запрос к базе данных завершился с ошибкой.
        """
        return self.db.read_currencies()

    def get_currency(self, currency_id: int) -> Optional[Dict[str, Any]]:
        """Получает одну валюту по её ID.
        
        Args:
            currency_id: ID валюты для получения.
        
        Returns:
            Словарь валюты или None, если не найдено.
        
        Raises:
            Exception: Если при запросе к базе данных произошла ошибка.
        """
        return self.db.read_currency(currency_id)

    def get_currency_by_code(self, char_code: str) -> Optional[Dict[str, Any]]:
        """Получает валюту по символьному коду.
        
        Args:
            char_code: Символьный код валюты (например, "USD").
        
        Returns:
            Словарь валюты или None, если не найдено.
        
        Raises:
            Exception: Если при запросе к базе данных произошла ошибка.
        """
        return self.db.read_currency_by_char_code(char_code)

    def add_currency(
        self,
        num_code: str,
        char_code: str,
        name: str,
        value: float,
        nominal: int
    ) -> int:
        """Создаёт новую запись о валюте.
        
        Args:
            num_code: Цифровой код валюты.
            char_code: Символьный код валюты.
            name: Название валюты.
            value: Значение курса обмена.
            nominal: Номинал валюты.
        
        Returns:
            ID недавно созданной валюты.
        
        Raises:
            Exception: Если операция с базой данных завершилась ошибкой.
        """
        return self.db.create_currency(num_code, char_code, name, value, nominal)

    def update_currency(self, currency_id: int, **kwargs: Any) -> bool:
        """Обновляет запись о валюте.
        
        Позволяет обновлять свойства валюты, такие как value, name, nominal и т.д.
        
        Args:
            currency_id: ID валюты для обновления.
            **kwargs: Поля для обновления (например, value=90.5, name="New name").
                     Поддерживаемые поля: num_code, char_code, name, value, nominal.
        
        Returns:
            True, если запись была обновлена, False если запись не найдена.
        
        Raises:
            ValueError: Если указаны недопустимые имена полей.
            Exception: Если операция с базой данных завершилась ошибкой.
        """
        return self.db.update_currency(currency_id, **kwargs)

    def update_currency_value(self, currency_id: int, new_value: float) -> bool:
        """Обновляет значение курса валюты.
        
        Удобный метод для обновления только поля value.
        
        Args:
            currency_id: ID валюты.
            new_value: Новое значение курса.
        
        Returns:
            True, если обновлено, False если валюта не найдена.
        
        Raises:
            Exception: Если операция с базой данных завершилась ошибкой.
        """
        return self.update_currency(currency_id, value=new_value)

    def update_currency_value_by_code(
        self,
        char_code: str,
        new_value: float
    ) -> bool:
        """Обновляет курс по символьному коду.
        
        Args:
            char_code: Символьный код валюты (например, "USD").
            new_value: Новое значение курса.
        
        Returns:
            True, если обновлено, False если валюта не найдена.
        
        Raises:
            Exception: Если операция с базой данных завершилась ошибкой.
        """
        currency = self.get_currency_by_code(char_code)
        if not currency:
            return False
        return self.update_currency_value(currency['id'], new_value)

    def delete_currency(self, currency_id: int) -> bool:
        """Удаляет валюту из базы данных.
        
        Каскадное удаление также удаляет подписки пользователей на эту валюту.
        
        Args:
            currency_id: ID валюты для удаления.
        
        Returns:
            True, если валюта удалена, False если не найдена.
        
        Raises:
            Exception: Если операция с базой данных завершилась ошибкой.
        """
        return self.db.delete_currency(currency_id)

    # ============= USER MANAGEMENT =============
    
    def list_users(self) -> List[Dict[str, Any]]:
        """Получает всех пользователей из базы данных.
        
        Returns:
            Список словарей пользователей с ключами: id, name.
        
        Raises:
            Exception: Если запрос к базе данных завершился ошибкой.
        """
        return self.db.read_users()

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получает одного пользователя по ID.
        
        Args:
            user_id: ID пользователя для получения.
        
        Returns:
            Словарь пользователя или None если не найден.
        
        Raises:
            Exception: Если при запросе к базе данных возникла ошибка.
        """
        return self.db.read_user(user_id)

    def add_user(self, name: str) -> int:
        """Создаёт новую запись пользователя.
        
        Args:
            name: Имя пользователя.
        
        Returns:
            ID созданного пользователя.
        
        Raises:
            Exception: Если операция с базой данных завершилась ошибкой.
        """
        return self.db.create_user(name)

    def update_user(self, user_id: int, name: str) -> bool:
        """Обновляет запись пользователя.
        
        Args:
            user_id: ID пользователя для обновления.
            name: Новое имя пользователя.
        
        Returns:
            True, если пользователь обновлён, False если не найден.
        
        Raises:
            Exception: Если операция с базой данных завершилась ошибкой.
        """
        return self.db.update_user(user_id, name)

    def delete_user(self, user_id: int) -> bool:
        """Удаляет пользователя из базы данных.
        
        Каскадное удаление удаляет все подписки для этого пользователя.
        
        Args:
            user_id: ID пользователя для удаления.
        
        Returns:
            True, если пользователь удалён, False если не найден.
        
        Raises:
            Exception: Если операция с базой данных завершилась ошибкой.
        """
        return self.db.delete_user(user_id)

    # ============= USER SUBSCRIPTION MANAGEMENT =============
    
    def subscribe_user_to_currency(self, user_id: int, currency_id: int) -> int:
        """Подписывает пользователя на валюту.
        
        Args:
            user_id: ID пользователя.
            currency_id: ID валюты.
        
        Returns:
            ID созданной записи подписки.
        
        Raises:
            Exception: Если операция с базой данных завершилась ошибкой (например, неверные внешние ключи).
        """
        return self.db.create_user_currency(user_id, currency_id)

    def get_user_currencies(self, user_id: int) -> List[Dict[str, Any]]:
        """Получает все валюты, на которые подписан пользователь.
        
        Args:
            user_id: ID пользователя.
        
        Returns:
            Список словарей валют.
        
        Raises:
            Exception: Если при запросе к базе данных произошла ошибка.
        """
        return self.db.read_user_currencies(user_id)

    def unsubscribe_user_from_currency(
        self,
        user_id: int,
        currency_id: int
    ) -> bool:
        """Отписывает пользователя от валюты.
        
        Args:
            user_id: ID пользователя.
            currency_id: ID валюты.
        
        Returns:
            True, если подписка удалена, False если не найдена.
        
        Raises:
            Exception: Если операция с базой данных завершилась ошибкой.
        """
        return self.db.delete_user_currency(user_id, currency_id)

    def get_all_subscriptions(self) -> List[Dict[str, Any]]:
        """Получает все подписки пользователей.
        
        Returns:
            Список словарей подписок с ключами: id, user_id, currency_id.
        
        Raises:
            Exception: Если при запросе к базе данных произошла ошибка.
        """
        return self.db.read_all_user_currencies()

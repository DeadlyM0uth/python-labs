"""Контроллер базы данных для операций CRUD с SQLite.

Этот модуль реализует слой доступа к данным (DAL) для управления валютами,
пользователями и их подписками с использованием SQLite и базы данных в памяти (:memory:).

Используются параметризованные запросы для защиты от SQL-инъекций.
Реализованы первичные ключи (PRIMARY KEY AUTOINCREMENT) и внешние ключи (FOREIGN KEY)
для обеспечения целостности данных и связей между таблицами.

Ключевые понятия:
    - PRIMARY KEY: Уникально идентифицирует каждую строку в таблице (автоинкремент)
    - FOREIGN KEY: Создаёт связи между таблицами, обеспечивает ссылочную целостность
    - Параметризованные запросы: Используйте ? или :name для предотвращения SQL-инъекций
"""

import sqlite3
from typing import List, Dict, Any, Optional, Tuple


class CurrencyRatesCRUD:
    """Контроллер базы данных для курсов валют и подписок пользователей.
    
    Реализует операции CRUD (создание, чтение, обновление, удаление) для:
    - currency: Информация о валюте (коды, название, курс, номинал)
    - user: Пользователи приложения
    - user_currency: Подписки пользователей на валюты (отношение многие-ко-многим)
    
    Использует SQLite с базой данных в памяти (:memory:) для хранения данных.
    Все операции используют параметризованные запросы для безопасности.
    """

    def __init__(self, db_path: str = ':memory:') -> None:
        """Инициализирует соединение с базой данных и создаёт таблицы.
        
        Создаёт следующие таблицы:
        - user: Хранит информацию о пользователях
        - currency: Хранит данные о валютах
        - user_currency: Связь "многие ко многим" между пользователями и валютами
        
        Args:
            db_path: Путь к файлу базы данных или ':memory:' для базы в памяти.
                    По умолчанию ':memory:' для целей тестирования.
        
        Raises:
            sqlite3.Error: Если инициализация базы данных не удалась.
        """
        self.conn: sqlite3.Connection = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Включаем доступ к колонкам по имени
        self._create_tables()

    def _create_tables(self) -> None:
        """Создаёт таблицы базы данных с корректной схемой.
        
        Создаваемые таблицы:
        1. user (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)
        2. currency (id INTEGER PRIMARY KEY AUTOINCREMENT, num_code TEXT NOT NULL,
                     char_code TEXT NOT NULL, name TEXT NOT NULL,
                     value FLOAT, nominal INTEGER)
        3. user_currency (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
                          currency_id INTEGER NOT NULL,
                          FOREIGN KEY(user_id) REFERENCES user(id),
                          FOREIGN KEY(currency_id) REFERENCES currency(id))
        
        Raises:
            sqlite3.Error: Если создание таблиц не удалось.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        # Создаём таблицу user
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        
        # Создаём таблицу currency
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL,
                name TEXT NOT NULL,
                value FLOAT,
                nominal INTEGER
            )
        ''')
        
        # Создаём таблицу user_currency
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE,
                FOREIGN KEY(currency_id) REFERENCES currency(id) ON DELETE CASCADE
            )
        ''')
        
        self.conn.commit()

    # ============= CURRENCY CRUD OPERATIONS =============
    
    def create_currency(
        self,
        num_code: str,
        char_code: str,
        name: str,
        value: float,
        nominal: int
    ) -> int:
        """Создаёт новую запись валюты.
        
        Args:
            num_code: Цифровой код валюты (например, "840" для USD).
            char_code: Символьный код валюты (например, "USD").
            name: Название валюты (например, "Доллар США").
            value: Значение курса обмена.
            nominal: Номинал (за сколько единиц указан курс).
        
        Returns:
            ID созданной записи валюты.
        
        Raises:
            sqlite3.Error: Если вставка записи не удалась.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        sql: str = '''
            INSERT INTO currency (num_code, char_code, name, value, nominal)
            VALUES (?, ?, ?, ?, ?)
        '''
        
        cursor.execute(sql, (num_code, char_code, name, value, nominal))
        self.conn.commit()
        
        return cursor.lastrowid

    def read_currencies(self) -> List[Dict[str, Any]]:
        """Читает все валюты из базы данных.
        
        Returns:
            Список словарей с информацией о валютах.
            Каждый словарь содержит ключи: id, num_code, char_code, name, value, nominal.
        
        Raises:
            sqlite3.Error: Если запрос не выполнен успешно.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        sql: str = 'SELECT * FROM currency'
        cursor.execute(sql)
        
        rows: List[sqlite3.Row] = cursor.fetchall()
        return [dict(row) for row in rows]

    def read_currency(self, currency_id: int) -> Optional[Dict[str, Any]]:
        """Читает одну валюту по ID.
        
        Args:
            currency_id: ID валюты для получения.
        
        Returns:
            Словарь с данными валюты или None, если не найдено.
            Ключи: id, num_code, char_code, name, value, nominal.
        
        Raises:
            sqlite3.Error: Если запрос не удался.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        sql: str = 'SELECT * FROM currency WHERE id = ?'
        cursor.execute(sql, (currency_id,))
        
        row: Optional[sqlite3.Row] = cursor.fetchone()
        return dict(row) if row else None

    def read_currency_by_char_code(self, char_code: str) -> Optional[Dict[str, Any]]:
        """Читает валюту по символьному коду.
        
        Args:
            char_code: Символьный код валюты (например, "USD").
        
        Returns:
            Словарь с данными валюты или None, если не найдено.
            Ключи: id, num_code, char_code, name, value, nominal.
        
        Raises:
            sqlite3.Error: Если запрос не удался.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        sql: str = 'SELECT * FROM currency WHERE char_code = ?'
        cursor.execute(sql, (char_code,))
        
        row: Optional[sqlite3.Row] = cursor.fetchone()
        return dict(row) if row else None

    def update_currency(self, currency_id: int, **kwargs: Any) -> bool:
        """Обновляет запись валюты.
        
        Args:
            currency_id: ID обновляемой валюты.
            **kwargs: Поля для обновления (value, name, nominal и т.д.).
                     Поддерживаемые: num_code, char_code, name, value, nominal.
        
        Returns:
            True, если запись была обновлена, False если не найдена.
        
        Raises:
            sqlite3.Error: Если обновление не удалось.
            ValueError: Если передано неподдерживаемое поле.
        """
        allowed_fields: Tuple[str, ...] = (
            'num_code', 'char_code', 'name', 'value', 'nominal'
        )
        
        for field in kwargs:
            if field not in allowed_fields:
                raise ValueError(f"Unsupported field: {field}")
        
        if not kwargs:
            return False
        
        # Build dynamic UPDATE query
        set_clauses: List[str] = [f"{field} = ?" for field in kwargs.keys()]
        set_sql: str = ', '.join(set_clauses)
        values: Tuple[Any, ...] = tuple(kwargs.values()) + (currency_id,)
        
        sql: str = f'UPDATE currency SET {set_sql} WHERE id = ?'
        
        cursor: sqlite3.Cursor = self.conn.cursor()
        cursor.execute(sql, values)
        self.conn.commit()
        
        return cursor.rowcount > 0

    def delete_currency(self, currency_id: int) -> bool:
        """Удаляет запись валюты.
        
        Каскадное удаление удаляет все записи user_currency для этой валюты.
        
        Args:
            currency_id: ID валюты для удаления.
        
        Returns:
            True, если запись удалена, False если не найдена.
        
        Raises:
            sqlite3.Error: Если удаление не удалось.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        sql: str = 'DELETE FROM currency WHERE id = ?'
        cursor.execute(sql, (currency_id,))
        self.conn.commit()
        
        return cursor.rowcount > 0

    # ============= USER CRUD OPERATIONS =============
    
    def create_user(self, name: str) -> int:
        """Создаёт новую запись пользователя.
        
        Args:
            name: Имя пользователя.
        
        Returns:
            ID созданной записи пользователя.
        
        Raises:
            sqlite3.Error: Если вставка не удалась.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        sql: str = 'INSERT INTO user (name) VALUES (?)'
        cursor.execute(sql, (name,))
        self.conn.commit()
        
        return cursor.lastrowid

    def read_users(self) -> List[Dict[str, Any]]:
        """Читает всех пользователей из базы данных.
        
        Returns:
            Список словарей с информацией о пользователях.
            Каждый словарь имеет ключи: id, name.
        
        Raises:
            sqlite3.Error: Если запрос не удался.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        sql: str = 'SELECT * FROM user'
        cursor.execute(sql)
        
        rows: List[sqlite3.Row] = cursor.fetchall()
        return [dict(row) for row in rows]

    def read_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Читает одного пользователя по ID.
        
        Args:
            user_id: ID пользователя для получения.
        
        Returns:
            Словарь с данными пользователя или None, если не найден.
            Ключи: id, name.
        
        Raises:
            sqlite3.Error: Если запрос не удался.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        sql: str = 'SELECT * FROM user WHERE id = ?'
        cursor.execute(sql, (user_id,))
        
        row: Optional[sqlite3.Row] = cursor.fetchone()
        return dict(row) if row else None

    def update_user(self, user_id: int, name: str) -> bool:
        """Обновляет запись пользователя.
        
        Args:
            user_id: ID пользователя для обновления.
            name: Новое имя пользователя.
        
        Returns:
            True, если запись обновлена, False если не найдена.
        
        Raises:
            sqlite3.Error: Если обновление не удалось.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        sql: str = 'UPDATE user SET name = ? WHERE id = ?'
        cursor.execute(sql, (name, user_id))
        self.conn.commit()
        
        return cursor.rowcount > 0

    def delete_user(self, user_id: int) -> bool:
        """Удаляет запись пользователя.
        
        Каскадное удаление удаляет все записи user_currency для этого пользователя.
        
        Args:
            user_id: ID пользователя для удаления.
        
        Returns:
            True, если запись удалена, False если не найдена.
        
        Raises:
            sqlite3.Error: Если удаление не удалось.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        sql: str = 'DELETE FROM user WHERE id = ?'
        cursor.execute(sql, (user_id,))
        self.conn.commit()
        
        return cursor.rowcount > 0

    # ============= USER_CURRENCY (SUBSCRIPTION) CRUD OPERATIONS =============
    
    def create_user_currency(self, user_id: int, currency_id: int) -> int:
        """Создаёт подписку пользователя на валюту.
        
        Args:
            user_id: ID пользователя (внешний ключ к user.id).
            currency_id: ID валюты (внешний ключ к currency.id).
        
        Returns:
            ID созданной записи подписки.
        
        Raises:
            sqlite3.Error: Если вставка не удалась (например, неверные внешние ключи).
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        sql: str = '''
            INSERT INTO user_currency (user_id, currency_id)
            VALUES (?, ?)
        '''
        
        cursor.execute(sql, (user_id, currency_id))
        self.conn.commit()
        
        return cursor.lastrowid

    def read_user_currencies(
        self,
        user_id: int
    ) -> List[Dict[str, Any]]:
        """Читает все валюты, на которые подписан указанный пользователь.
        
        Args:
            user_id: ID пользователя.
        
        Returns:
            Список словарей валют, на которые подписан пользователь.
            Каждый словарь содержит ключи из таблицы currency: id, num_code, char_code, name, value, nominal.
        
        Raises:
            sqlite3.Error: Если запрос не удался.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        sql: str = '''
            SELECT c.*
            FROM currency c
            INNER JOIN user_currency uc ON c.id = uc.currency_id
            WHERE uc.user_id = ?
        '''
        
        cursor.execute(sql, (user_id,))
        rows: List[sqlite3.Row] = cursor.fetchall()
        return [dict(row) for row in rows]

    def read_all_user_currencies(self) -> List[Dict[str, Any]]:
        """Читает все записи подписок (user_currency).
        
        Returns:
            Список словарей с ключами: id, user_id, currency_id.
        
        Raises:
            sqlite3.Error: Если запрос не удался.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        sql: str = 'SELECT * FROM user_currency'
        cursor.execute(sql)
        
        rows: List[sqlite3.Row] = cursor.fetchall()
        return [dict(row) for row in rows]

    def delete_user_currency(self, user_id: int, currency_id: int) -> bool:
        """Удаляет подписку пользователя на валюту.
        
        Args:
            user_id: ID пользователя.
            currency_id: ID валюты.
        
        Returns:
            True, если подписка удалена, False если не найдена.
        
        Raises:
            sqlite3.Error: Если удаление не удалось.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        sql: str = '''
            DELETE FROM user_currency
            WHERE user_id = ? AND currency_id = ?
        '''
        
        cursor.execute(sql, (user_id, currency_id))
        self.conn.commit()
        
        return cursor.rowcount > 0

    def delete_user_currency_by_id(self, uc_id: int) -> bool:
        """Удаляет запись подписки по ID.
        
        Args:
            uc_id: ID записи user_currency для удаления.
        
        Returns:
            True, если запись удалена, False если не найдена.
        
        Raises:
            sqlite3.Error: Если удаление не удалось.
        """
        cursor: sqlite3.Cursor = self.conn.cursor()
        
        sql: str = 'DELETE FROM user_currency WHERE id = ?'
        cursor.execute(sql, (uc_id,))
        self.conn.commit()
        
        return cursor.rowcount > 0

    def close(self) -> None:
        """Закрывает соединение с базой данных.
        
        Raises:
            sqlite3.Error: Если закрытие соединения не удалось.
        """
        if self.conn:
            self.conn.close()

    def __enter__(self) -> 'CurrencyRatesCRUD':
        """Точка входа менеджера контекста.
        
        Returns:
            Self для использования в операторе 'with'.
        """
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Точка выхода менеджера контекста.
        
        Закрывает соединение с базой данных при выходе из контекста.
        
        Args:
            exc_type: Тип исключения, если есть.
            exc_val: Значение исключения, если есть.
            exc_tb: Трассировка исключения, если есть.
        """
        self.close()

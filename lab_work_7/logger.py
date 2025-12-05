"""
Модуль с логирующим декоратором.

Декоратор для логирования вызовов функций, поддерживающий разные типы логгеров.
"""

import sys
import io
import logging
from functools import wraps
from typing import Any, Callable, Optional, Union, TextIO, Type
from datetime import datetime


def logger(
    func: Optional[Callable] = None,
    *,
    handle: Union[TextIO, io.StringIO, logging.Logger] = sys.stdout
) -> Callable:
    """
    Параметризуемый декоратор для логирования вызовов функций.
    
    Args:
        func: Декорируемая функция (используется при вызове без скобок)
        handle: Объект для логирования. Может быть:
            - sys.stdout (по умолчанию)
            - любой объект с методом write() (например, io.StringIO)
            - logging.Logger для использования модуля logging
    
    Returns:
        Декорированная функция с логированием.
        
    Examples:
        >>> # Логирование в stdout
        >>> @logger
        >>> def my_func(x):
        >>>     return x * 2
        >>>
        >>> # Логирование в StringIO
        >>> stream = io.StringIO()
        >>> @logger(handle=stream)
        >>> def my_func(x):
        >>>     return x * 2
        >>>
        >>> # Логирование через logging
        >>> log = logging.getLogger("my_logger")
        >>> @logger(handle=log)
        >>> def my_func(x):
        >>>     return x * 2
    """
    
    def decorator(inner_func: Callable) -> Callable:
        @wraps(inner_func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Подготовка информации о вызове
            func_name = inner_func.__name__
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Логирование начала вызова
            start_message = f"[{timestamp}] INFO: Вызов функции {func_name} с args={args}, kwargs={kwargs}"
            
            if isinstance(handle, logging.Logger):
                handle.info(start_message)
            else:
                handle.write(start_message + "\n")
            
            try:
                # Выполнение функции
                result = inner_func(*args, **kwargs)
                
                # Логирование успешного завершения
                success_message = f"[{timestamp}] INFO: Функция {func_name} успешно завершилась. Результат: {result}"
                
                if isinstance(handle, logging.Logger):
                    handle.info(success_message)
                else:
                    handle.write(success_message + "\n")
                
                return result
                
            except Exception as e:
                # Логирование ошибки
                error_message = f"[{timestamp}] ERROR: В функции {func_name} возникло исключение {type(e).__name__}: {str(e)}"
                
                if isinstance(handle, logging.Logger):
                    handle.error(error_message)
                else:
                    handle.write(error_message + "\n")
                
                # Пробрасываем исключение дальше
                raise
        
        return wrapper
    
    # Обработка вызова декоратора с аргументами и без
    if func is None:
        return decorator
    else:
        return decorator(func)
"""
Настройка логирования в файл для функции get_currencies.
"""

import logging
from logger import logger
from currencies import get_currencies
from typing import Dict, List

def setup_file_logging() -> logging.Logger:
    """
    Настраивает логирование в файл.
    
    Returns:
        Настроенный логгер для записи в файл.
    """
    # Создаем логгер
    logger = logging.getLogger("currency_file")
    logger.setLevel(logging.DEBUG)
    
    # Создаем обработчик для записи в файл
    file_handler = logging.FileHandler("currency.log", encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Настраиваем формат сообщений
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)
    
    return logger


# Создаем логгер для файла
file_logger = setup_file_logging()


@logger(handle=file_logger)
def get_currencies_file_logged(
    currency_codes: List[str],
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
    timeout: float = 10.0
) -> Dict[str, float]:
    """Версия функции get_currencies с логированием в файл."""
    return get_currencies(currency_codes, url, timeout)

    
if __name__ == "__main__":
  get_currencies_file_logged(currency_codes=["USD"])
      
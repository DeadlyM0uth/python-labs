"""
Модуль для работы с курсами валют ЦБ РФ.

Содержит функцию для получения курсов валют через API Центрального банка.
"""

import json
import sys
from logger import logger
from typing import Dict, List
from urllib import request
from urllib.error import URLError


def get_currencies(
    currency_codes: List[str],
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
    timeout: float = 10.0
) -> Dict[str, float]:
    """
    Получает курсы валют от API Центрального банка РФ.
    
    Args:
        currency_codes: Список кодов валют для получения (например, ["USD", "EUR"])
        url: URL API Центрального банка (по умолчанию используется тестовый endpoint)
        timeout: Таймаут запроса в секундах
    
    Returns:
        Словарь с кодами валют и их курсами, например: {"USD": 93.25, "EUR": 101.7}
    
    Raises:
        ConnectionError: Если API недоступен или произошла ошибка сети
        ValueError: Если получен некорректный JSON
        KeyError: Если в ответе отсутствует ключ "Valute" или запрашиваемая валюта
        TypeError: Если курс валюты имеет неверный тип (не число)
    
    Examples:
        >>> get_currencies(["USD", "EUR"])
        {'USD': 93.25, 'EUR': 101.7}
    """
    
    try:
        # Выполнение запроса к API
        with request.urlopen(url, timeout=timeout) as response:
            data = response.read().decode('utf-8')
    except (URLError, TimeoutError) as e:
        raise ConnectionError(f"Ошибка подключения к API: {e}")
    
    try:
        # Парсинг JSON
        json_data = json.loads(data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Некорректный JSON от API: {e}")
    
    # Проверка наличия ключа "Valute"
    if "Valute" not in json_data:
        raise KeyError("В ответе API отсутствует ключ 'Valute'")
    
    valute_data = json_data["Valute"]
    result = {}
    
    # Извлечение курсов для запрошенных валют
    for code in currency_codes:
        if code not in valute_data:
            raise KeyError(f"Валюта {code} отсутствует в данных API")
        
        currency_info = valute_data[code]
        
        # Проверка типа значения курса
        if not isinstance(currency_info.get("Value"), (int, float)):
            raise TypeError(
                f"Курс валюты {code} имеет неверный тип: {type(currency_info.get('Value'))}"
            )
        
        result[code] = round(currency_info["Value"], 2)
    
    return result


# Обертываем функцию декоратором
@logger(handle=sys.stdout)
def get_currencies_logged(
    currency_codes: List[str],
    url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
    timeout: float = 10.0
) -> Dict[str, float]:
    """Версия функции get_currencies с логированием."""
    return get_currencies(currency_codes, url, timeout)

    
if __name__ == "__main__":
  get_currencies_logged(currency_codes=["USD"])
"""Утилита для получения курсов валют.

Содержит функцию для получения актуальных курсов валют
от Центрального банка Российской Федерации.
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Any
import urllib.request
import urllib.error


def get_currencies() -> List[Dict[str, Any]]:
    """Получает список валют от Центрального банка РФ.
    
    Используется API Центрального банка Российской Федерации.
    
    Returns:
        
        Cписок словарей с информацией о валютах. Каждый словарь содержит:
        - 'id': уникальный идентификатор валюты
        - 'num_code': цифровой код (NumCode)
        - 'char_code': символьный код (CharCode)
        - 'name': название валюты (Name)
        - 'value': текущий курс (Value)
        - 'nominal': номинал (Nominal)
        
    Raises:
        urllib.error.URLError: Если не удаётся подключиться к API.
        urllib.error.HTTPError: Если сервер возвращает HTTP ошибку.
        ET.ParseError: Если полученный XML некорректен.
        ValueError: Если в XML отсутствуют необходимые поля.
    
    Example:
        >>> currencies = get_currencies()
        >>> if currencies:
        ...     print(f"USD: {currencies[0]['value']}")
    """
    url = "https://www.cbr-xml-daily.ru/daily.xml"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            xml_bytes = response.read()
            # Пытаемся декодировать с разными кодировками
            for encoding in ['windows-1251', 'utf-8', 'cp1251', 'iso-8859-5']:
                try:
                    xml_data = xml_bytes.decode(encoding)
                    break
                except (UnicodeDecodeError, AttributeError):
                    continue
            else:
                # Если ничего не подошло, используем utf-8 с игнорированием ошибок
                xml_data = xml_bytes.decode('utf-8', errors='ignore')
    except urllib.error.URLError as e:
        raise urllib.error.URLError(f"Не удаётся подключиться к API валют: {e}") from e
    except urllib.error.HTTPError as e:
        raise urllib.error.HTTPError(
            e.url,
            e.code,
            f"Ошибка сервера при получении курсов валют: {e.reason}",
            e.hdrs,
            e.fp,
        ) from e
    
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        raise ET.ParseError(f"Ошибка при разборе XML: {e}") from e
    
    currencies = []
    
    # Ищем все элементы Valute в XML
    for valute in root.findall('Valute'):
        try:
            # Извлекаем данные из элементов
            valute_id = valute.get('ID')
            num_code = valute.findtext('NumCode')
            char_code = valute.findtext('CharCode')
            name = valute.findtext('Name')
            value = valute.findtext('Value')
            nominal = valute.findtext('Nominal')
            
            # Проверяем наличие всех необходимых полей
            if not all([valute_id, num_code, char_code, name, value, nominal]):
                raise ValueError(f"Неполные данные для валюты {valute_id}")
            
            currencies.append({
                'id': valute_id,
                'num_code': num_code,
                'char_code': char_code,
                'name': name,
                'value': value,
                'nominal': nominal,
            })
        except (AttributeError, ValueError) as e:
            # Логируем ошибку для конкретной валюты и продолжаем обработку
            print(f"Предупреждение: Не удаётся обработать валюту {valute.get('ID')}: {e}")
            continue
    
    if not currencies:
        raise ValueError("В полученном XML не найдены валюты")
    
    return currencies


def get_currencies_by_code(
    code: str,
    currencies: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any] | None:
    """Получает валюту по символьному коду.
    
    Args:
        code: Символьный код валюты (например, 'USD', 'EUR').
        currencies: Список валют. Если None, будет выполнен запрос к API.
        
    Returns:
        Словарь с информацией о валюте или None, если валюта не найдена.
        
    Raises:
        urllib.error.URLError: Если не удаётся получить список валют.
        ValueError: Если полученные данные некорректны.
    
    Example:
        >>> usd = get_currencies_by_code('USD')
        >>> if usd:
        ...     print(usd['value'])
    """
    if currencies is None:
        currencies = get_currencies()
    
    code_upper = code.upper()
    
    for currency in currencies:
        if currency['char_code'].upper() == code_upper:
            return currency
    
    return None

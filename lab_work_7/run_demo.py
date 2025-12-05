"""
Главный модуль для демонстрации работы лабораторной работы.
"""

import sys
import logging
from typing import NoReturn
from demo_quadratic_equation import demonstrate_quadratic
from currencies import get_currencies_logged
from currencies_file_logged import get_currencies_file_logged

def main() -> NoReturn:
    """
    Основная функция для демонстрации работы всех компонентов.
    
    Запускает демонстрационные примеры и тесты.
    """
    print("Лабораторная работа 7: Логирование и обработка ошибок в Python")
    print("=" * 60)
    
    # Демонстрация квадратного уравнения
    demonstrate_quadratic()
    
    print("\n" + "=" * 60)
    print("Демонстрация работы с валютами")
    print("=" * 60)
    
    # Демонстрация работы с валютами
    try:
        # Используем декорированную версию
        result = get_currencies_logged(["USD", "EUR"])
        print(f"\nКурсы валют: {result}")
    except Exception as e:
        print(f"\nОшибка при получении курсов валют: {e}")
    
    # Демонстрация логирования в файл
    print("\n" + "=" * 60)
    print("Логирование в файл")
    print("=" * 60)
    
    try:
        result = get_currencies_file_logged(["USD", "EUR"])
        print(f"Курсы валют (залогировано в файл): {result}")
        print("Логи записаны в файл 'currency.log'")
    except Exception as e:
        print(f"Ошибка: {e}")
    


if __name__ == "__main__":
    main()
"""
Демонстрационный пример с квадратным уравнением.

Показывает использование логирующего декоратора с разными уровнями логирования.
"""

import math
from logger import logger
from typing import Tuple, Optional, Union


@logger
def solve_quadratic(
    a: Union[int, float],
    b: Union[int, float],
    c: Union[int, float]
) -> Optional[Tuple[float, ...]]:
    """
    Решает квадратное уравнение ax² + bx + c = 0.
    
    Args:
        a: Коэффициент при x²
        b: Коэффициент при x
        c: Свободный член
    
    Returns:
        Кортеж с корнями уравнения или None, если корней нет.
    
    Raises:
        TypeError: Если коэффициенты не числовые
        ValueError: Если a = 0 и b = 0 (бессмысленное уравнение)
    """
    # Проверка типов
    if not all(isinstance(coef, (int, float)) for coef in (a, b, c)):
        raise TypeError("Все коэффициенты должны быть числами")
    
    # Проверка на критическую ситуацию
    if a == 0 and b == 0:
        raise ValueError("Уравнение 0 = c не имеет смысла при c ≠ 0")
    
    # Если a = 0, это линейное уравнение
    if a == 0:
        if b == 0:
            return None
        x = -c / b
        return (x,)
    
    # Вычисление дискриминанта
    discriminant = b**2 - 4*a*c
    
    # Обработка отрицательного дискриминанта
    if discriminant < 0:
        # Генерируем предупреждение через исключение
        # (в реальном коде использовали бы warnings.warn)
        print(f"WARNING: Дискриминант отрицательный: D = {discriminant}")
        return None
    
    # Вычисление корней
    sqrt_d = math.sqrt(discriminant)
    x1 = (-b + sqrt_d) / (2*a)
    x2 = (-b - sqrt_d) / (2*a)
    
    # Если корни совпадают, возвращаем один корень
    if math.isclose(x1, x2):
        return (x1,)
    
    return (x1, x2)


# Пример использования с разными сценариями
def demonstrate_quadratic() -> None:
    """Демонстрация работы функции solve_quadratic."""
    
    print("\n" + "="*50)
    print("Демонстрация квадратного уравнения")
    print("="*50)
    
    # Сценарий 1: Два корня (INFO)
    print("\n1. Два корня:")
    try:
        result = solve_quadratic(1, -3, 2)
        print(f"   Результат: {result}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    # Сценарий 2: Один корень (INFO)
    print("\n2. Один корень:")
    try:
        result = solve_quadratic(1, -4, 4)
        print(f"   Результат: {result}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    # Сценарий 3: Отрицательный дискриминант (WARNING)
    print("\n3. Отрицательный дискриминант:")
    try:
        result = solve_quadratic(1, 2, 5)
        print(f"   Результат: {result}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    # Сценарий 4: Некорректные данные (ERROR)
    print("\n4. Некорректные данные (строка вместо числа):")
    try:
        result = solve_quadratic("abc", 2, 3)
        print(f"   Результат: {result}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    # Сценарий 5: Критическая ситуация (CRITICAL)
    print("\n5. Критическая ситуация (a=0, b=0):")
    try:
        result = solve_quadratic(0, 0, 5)
        print(f"   Результат: {result}")
    except Exception as e:
        print(f"   Ошибка: {e}")
        
        
if __name__ == "__main__":
  demonstrate_quadratic()
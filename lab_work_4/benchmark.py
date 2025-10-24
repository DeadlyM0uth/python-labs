"""
Сравнение времени выполнения рекурсивного и итеративного вычисления факториала.

Модуль демонстрирует различие в эффективности двух реализаций:
- рекурсивной (fact_recursive)
- нерекурсивной (fact_iterative)

Для оценки производительности используется модуль `timeit`, а результаты
визуализируются с помощью `matplotlib`.

Автор: Смирнов Вадим
Дата: 2025-10-25
"""

import timeit
import matplotlib.pyplot as plt
from typing import List


def fact_recursive(n: int) -> int:
    """
    Вычисляет факториал числа рекурсивно.

    Args:
        n (int): Число, для которого вычисляется факториал. Должно быть >= 0.

    Returns:
        int: Факториал числа n.

    Raises:
        ValueError: Если n < 0.
    """
    if n < 0:
        raise ValueError("Аргумент должен быть неотрицательным")
    if n in (0, 1):
        return 1
    return n * fact_recursive(n - 1)


def fact_iterative(n: int) -> int:
    """
    Вычисляет факториал числа итеративно (через цикл).

    Args:
        n (int): Число, для которого вычисляется факториал. Должно быть >= 0.

    Returns:
        int: Факториал числа n.

    Raises:
        ValueError: Если n < 0.
    """
    if n < 0:
        raise ValueError("Аргумент должен быть неотрицательным")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def benchmark_factorial(func_name: str, numbers: List[int], repeat: int = 5) -> List[float]:
    """
    Измеряет среднее время выполнения функции вычисления факториала.

    Args:
        func_name (str): Имя функции ('fact_recursive' или 'fact_iterative').
        numbers (List[int]): Список чисел для тестирования.
        repeat (int): Количество повторов для усреднения.

    Returns:
        List[float]: Среднее время выполнения для каждого числа.
    """
    results = []
    for n in numbers:
        stmt = f"{func_name}({n})"
        setup = f"from __main__ import {func_name}"
        # timeit.timeit возвращает общее время выполнения указанного количества прогонов.
        time_taken = timeit.timeit(stmt, setup=setup, number=repeat)
        avg_time = time_taken / repeat
        results.append(avg_time)
    return results


def main() -> None:
    """Основная функция программы: выполняет бенчмарк и строит график."""
    # Фиксированный набор чисел
    numbers = list(range(1, 501, 50))  # n = 1, 51, 101, ..., 451

    # Измерение времени выполнения
    recursive_times = benchmark_factorial("fact_recursive", numbers)
    iterative_times = benchmark_factorial("fact_iterative", numbers)

    # Визуализация результатов
    plt.figure(figsize=(10, 6))
    plt.plot(numbers, recursive_times, marker="o", label="Рекурсивный способ")
    plt.plot(numbers, iterative_times, marker="s", label="Итеративный способ")
    plt.title("Сравнение времени вычисления факториала")
    plt.xlabel("Входное число n")
    plt.ylabel("Среднее время выполнения (секунды)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

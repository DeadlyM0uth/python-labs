"""
Сравнение времени построения бинарного дерева рекурсивным и итеративным способами.

Вариант №11:
  root = 11
  height = 3
  left_leaf = root ** 2
  right_leaf = 2 + root ** 2

Задача:
  1. Реализовать две функции построения бинарного дерева:
      - рекурсивную (build_tree_recursive)
      - итеративную (build_tree_iterative)
  2. Сравнить их время работы при разных высотах дерева.
  3. Построить график зависимости времени от высоты дерева.
  4. Сделать выводы о производительности.

Автор: Смирнов Вадим
Дата: 2025-10-25
"""

from typing import Any, Dict, Optional, Callable
from collections import deque
import timeit
import matplotlib.pyplot as plt
import pprint



def build_tree_recursive(height: int, root: int) -> Optional[Dict[str, Any]]:
    """
    Рекурсивно строит бинарное дерево заданной высоты.

    Args:
        height (int): Высота дерева (>= 1). Если меньше 1 — возвращает None.
        root (int): Значение корня.

    Returns:
        Optional[Dict[str, Any]]: Бинарное дерево в виде словаря:
            {
              "value": root,
              "left": <левое поддерево>,
              "right": <правое поддерево>
            }

    Example:
        >>> build_tree_recursive(2, 11)
        {'value': 11, 'left': {'value': 121, 'left': None, 'right': None},
                       'right': {'value': 123, 'left': None, 'right': None}}
    """
    if height < 1:
        return None

    left_val = root ** 2
    right_val = 2 + root ** 2

    return {
        "value": root,
        "left": build_tree_recursive(height - 1, left_val),
        "right": build_tree_recursive(height - 1, right_val)
    }




def build_tree_iterative(height: int, root: int) -> Optional[Dict[str, Any]]:
    """
    Итеративно строит бинарное дерево заданной высоты с использованием очереди.

    Args:
        height (int): Высота дерева (>= 1).
        root (int): Значение корня.

    Returns:
        Optional[Dict[str, Any]]: Бинарное дерево в виде словаря.

    Example:
        >>> build_tree_iterative(2, 11)
        {'value': 11, 'left': {'value': 121, 'left': None, 'right': None},
                       'right': {'value': 123, 'left': None, 'right': None}}
    """
    if height < 1:
        return None

    tree = {"value": root, "left": None, "right": None}
    queue = deque([(tree, 1)])  # очередь узлов и уровня

    while queue:
        node, level = queue.popleft()
        if level < height:
            left_val = node["value"] ** 2
            right_val = 2 + node["value"] ** 2

            node["left"] = {"value": left_val, "left": None, "right": None}
            node["right"] = {"value": right_val, "left": None, "right": None}

            queue.append((node["left"], level + 1))
            queue.append((node["right"], level + 1))

    return tree




def measure_time():
    """
    Измеряет и сравнивает время построения дерева для разных высот
    между рекурсивной и итеративной реализациями.
    """
    heights = range(1, 12)  # тестируем от 1 до 11 уровней
    rec_times = []
    iter_times = []

    for h in heights:
        rec_t = timeit.timeit(lambda: build_tree_recursive(h, 11), number=100)
        iter_t = timeit.timeit(lambda: build_tree_iterative(h, 11), number=100)

        rec_times.append(rec_t)
        iter_times.append(iter_t)

        print(f"Высота={h}: рекурсивно={rec_t:.6f} с, итеративно={iter_t:.6f} с")

    # Построение графика
    plt.figure(figsize=(8, 5))
    plt.plot(heights, rec_times, marker='o', label='Рекурсивная версия')
    plt.plot(heights, iter_times, marker='s', label='Итеративная версия')
    plt.title('Сравнение времени построения бинарного дерева')
    plt.xlabel('Высота дерева')
    plt.ylabel('Время (сек)')
    plt.grid(True)
    plt.legend()
    plt.show()




if __name__ == "__main__":
    print("Пример дерева (высота=3, root=11):")
    pprint.pprint(build_tree_recursive(3, 11))
    print("\n--- Сравнение времени ---")
    measure_time()
from typing import Callable, Any, Dict, Optional
from collections import deque
import pprint

def gen_bin_tree(
    height: int = 3,
    root: Any = 11,
    left_branch: Callable[[Any], Any] = lambda x: x ** 2,
    right_branch: Callable[[Any], Any] = lambda x: 2 + x ** 2
) -> Dict[str, Any]:
    """
    Генерация бинарного дерева в виде словаря (нерекурсивно).

    Args:
        height (int): Высота дерева (число уровней, включая корень).
        root (Any): Значение корня дерева.
        left_branch (Callable[[Any], Any]): Функция для вычисления левого потомка.
        right_branch (Callable[[Any], Any]): Функция для вычисления правого потомка.

    Returns:
        tree (Dict[str, Any]): Бинарное дерево в виде вложенных словарей формата:
            {"value": <root>, "left": <левое поддерево>, "right": <правое поддерево>}

    Examples:
        >>> gen_bin_tree(height=3, root=11)
        {'value': 11, 'left': {'value': 121, 'left': {...}, 'right': {...}}, 'right': {...}}
    """

    if height <= 0:
      return None

    tree: Dict[str, Optional[Any]] = {"value": root, "left": None, "right": None}
    queue = deque([(tree, 1)])  # Очередь для обхода уровней: (узел, текущая_высота)

    while queue:
        node, level = queue.popleft()

        if level < height:
            left_val = left_branch(node["value"])
            right_val = right_branch(node["value"])

            # Создаём потомков
            node["left"] = {"value": left_val, "left": None, "right": None}
            node["right"] = {"value": right_val, "left": None, "right": None}

            # Добавляем потомков в очередь для дальнейшей обработки
            queue.append((node["left"], level + 1))
            queue.append((node["right"], level + 1))

    return tree


if __name__ == "__main__":
    tree = gen_bin_tree()  # height=3, root=11 по умолчанию
    print("Сгенерированное бинарное дерево:")
    pprint.pprint(tree)

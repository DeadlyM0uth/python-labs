from typing import Optional, Dict, Any
import pprint

def gen_bin_tree(height: int = 3, root: int = 11) -> Optional[Dict[str, Any]]:
  """Рекурсивно строит бинарное дерево заданной высоты и корневого значения.
  
  Генерирует бинарное дерево, где каждый узел содержит числовое значение,
  а левый и правый потомки вычисляются по формулам:
  - left = root²
  - right = 2 + root²
  
  Args:
    height (int): Высота дерева. Должна быть >= 1. 
                  Если height < 1, возвращается None.
      Default: 3
    root (int): Начальное значение корневого узла. 
      Default: 11
  
  Returns:
      
      Optional[Dict[str, Any]]: Словарь представляющий бинарное дерево 
                                в формате:
        {
          "value": int,           # значение текущего узла
          "left": Dict | None,    # левое поддерево
          "right": Dict | None    # правое поддерево
        }
      Возвращает None если height < 1.
  
  Raises:
      RecursionError: Если высота дерева слишком большая и превышает
                      максимальную глубину рекурсии Python.
  
  Examples:
    >>> tree = gen_bin_tree(height=2, root=2)
    >>> tree
    {
      'value': 2,
      'left': {
        'value': 4,
        'left': None,
        'right': None
      },
      'right': {
        'value': 6,
        'left': None,
        'right': None
      }
    }
    
    >>> gen_bin_tree(height=0)
    None
  
  Note:
    Значения узлов растут экспоненциально с увеличением высоты,
    что может привести к очень большим числам при height > 5.
  """
  if height < 1:
    return None

  left_value = root ** 2
  right_value = 2 + root ** 2

  tree = {
    "value": root,
    "left": gen_bin_tree(height - 1, left_value),
    "right": gen_bin_tree(height - 1, right_value)
  }

  return tree


if __name__ == "__main__":
  tree = gen_bin_tree(height=3, root=11)
  pprint.pprint(tree)
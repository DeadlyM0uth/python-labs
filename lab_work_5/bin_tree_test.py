import unittest
from typing import Optional, Dict, Any
from bin_tree import gen_bin_tree 


class TestGenBinTree(unittest.TestCase):
    """Набор тестов для функции gen_bin_tree.
    
    Тесты покрывают различные сценарии работы функции, включая граничные случаи,
    корректность структуры дерева и правильность вычисления значений узлов.
    """
    
    def test_height_zero_returns_none(self) -> None:
        """Тестирует случай, когда высота дерева равна 0.
        
        Ожидается, что функция вернет None при height = 0.
        """
        result = gen_bin_tree(height=0, root=11)
        self.assertIsNone(result)
    
    def test_negative_height_returns_none(self) -> None:
        """Тестирует случай, когда высота дерева отрицательна.
        
        Ожидается, что функция вернет None при height < 0.
        """
        result = gen_bin_tree(height=-1, root=11)
        self.assertIsNone(result)
    
    def test_height_one_returns_only_root(self) -> None:
        """Тестирует построение дерева высоты 1.
        
        Ожидается дерево только с корневым узлом без потомков.
        """
        result = gen_bin_tree(height=1, root=5)
        
        expected = {
          "value": 5,
          "left": None,
          "right": None
        }
        
        self.assertEqual(result, expected)
    
    def test_height_two_correct_structure(self) -> None:
        """Тестирует построение дерева высоты 2.
        
        Проверяет корректность структуры дерева и вычисления значений потомков.
        """
        root_val = 2
        left_val = root_val ** 2  # 4
        right_val = 2 + root_val ** 2  # 6
        
        result = gen_bin_tree(height=2, root=root_val)
        
        expected = {
          "value": root_val,
          "left": {
            "value": left_val,
            "left": None,
            "right": None
          },
          "right": {
            "value": right_val,
            "left": None,
            "right": None
          }
        }
        
        self.assertEqual(result, expected)
    
    def test_height_three_complex_structure(self) -> None:
      """Тестирует построение дерева высоты 3.
      
      Проверяет корректность многоуровневой структуры дерева
      и правильность вычисления значений на всех уровнях.
      """
      root_val = 2
      left_val = root_val ** 2  # 4
      right_val = 2 + root_val ** 2  # 6
      
      left_left_val = left_val ** 2  # 16
      left_right_val = 2 + left_val ** 2  # 18
      right_left_val = right_val ** 2  # 36
      right_right_val = 2 + right_val ** 2  # 38
      
      result = gen_bin_tree(height=3, root=root_val)
      
      expected = {
        "value": root_val,
        "left": {
          "value": left_val,
          "left": {
            "value": left_left_val,
            "left": None,
            "right": None
          },
          "right": {
            "value": left_right_val,
            "left": None,
            "right": None
          }
        },
        "right": {
          "value": right_val,
          "left": {
            "value": right_left_val,
            "left": None,
            "right": None
          },
          "right": {
            "value": right_right_val,
            "left": None,
            "right": None
          }
        }
      }
      
      self.assertEqual(result, expected)
    
    def test_different_root_values(self) -> None:
      """Тестирует построение деревьев с различными корневыми значениями.
      
      Проверяет, что функция корректно работает с разными начальными значениями.
      """
      test_cases = [1, 3, 10, 0, -2]
      
      for root_val in test_cases:
        with self.subTest(root=root_val):
          result = gen_bin_tree(height=2, root=root_val)
          
          # Проверяем корневое значение
          self.assertEqual(result["value"], root_val)
          
          # Проверяем левого потомка
          expected_left = root_val ** 2
          self.assertEqual(result["left"]["value"], expected_left)
          
          # Проверяем правого потомка
          expected_right = 2 + root_val ** 2
          self.assertEqual(result["right"]["value"], expected_right)
    
    def test_tree_structure_integrity(self) -> None:
        """Тестирует целостность структуры дерева.
        
        Проверяет, что все узлы имеют правильную структуру (value, left, right)
        и что листья правильно обозначены как None.
        """
        result = gen_bin_tree(height=3, root=3)
        
        def validate_tree_structure(node: Optional[Dict[str, Any]]) -> bool:
          """Рекурсивно проверяет структуру узла дерева."""
          if node is None:
            return True
          
          # Проверяем наличие обязательных ключей
          required_keys = {"value", "left", "right"}
          if not all(key in node for key in required_keys):
            return False
          
          # Проверяем типы значений
          if not isinstance(node["value"], int):
            return False
          
          # Рекурсивно проверяем потомков
          return (validate_tree_structure(node["left"]) and 
            validate_tree_structure(node["right"]))
        
        self.assertTrue(validate_tree_structure(result))
    
    def test_values_calculation_correctness(self) -> None:
        """Тестирует правильность вычисления значений в дереве.
        
        Рекурсивно проверяет, что значения потомков вычислены по заданным формулам.
        """
        result = gen_bin_tree(height=4, root=2)
        
        def validate_values_calculation(node: Dict[str, Any]) -> bool:
          """Рекурсивно проверяет корректность вычисления значений."""
          if node["left"] is not None:
            expected_left = node["value"] ** 2
            if node["left"]["value"] != expected_left:
              return False
            if not validate_values_calculation(node["left"]):
              return False
          
          if node["right"] is not None:
            expected_right = 2 + node["value"] ** 2
            if node["right"]["value"] != expected_right:
              return False
            if not validate_values_calculation(node["right"]):
              return False
          
          return True
        
        self.assertTrue(validate_values_calculation(result))
    
    def test_default_parameters(self) -> None:
      """Тестирует работу функции с параметрами по умолчанию.
      
      Проверяет, что функция корректно работает при вызове без аргументов.
      """
      result = gen_bin_tree()
      
      # Проверяем, что результат не None (высота по умолчанию = 3)
      self.assertIsNotNone(result)
      
      # Проверяем корневое значение по умолчанию
      self.assertEqual(result["value"], 11)
      
      # Проверяем, что дерево имеет ожидаемую глубину
      self.assertIsNotNone(result["left"]["left"])  # должен существовать
      self.assertIsNotNone(result["right"]["left"])  # должен существовать


if __name__ == "__main__":
    unittest.main(verbosity=2)
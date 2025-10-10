import unittest
# замените your_module на имя вашего файла
from guess_number import guess_number


class TestGuessNumber(unittest.TestCase):
  """Набор тестов для функции guess_number.

  Тестирует различные сценарии работы алгоритмов поиска:
    - Успешный поиск элементов в разных позициях
    - Обработка случаев когда элемент не найден
    - Работа с несортированными списками
    - Граничные случаи (пустой список, один элемент)
    - Обработка некорректных входных данных
  """

  def test_binary_search_found(self):
    """Тест бинарного поиска: число найдено в середине списка.

    Проверяет что:
      - Число успешно находится в отсортированном списке
      - Количество попыток больше нуля
      - Возвращается корректное найденное число
    """
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result, attempts = guess_number(5, numbers, 'binary')
    self.assertEqual(result, 5)
    self.assertGreater(attempts, 0)

  def test_linear_search_found(self):
    """Тест линейного поиска: число найдено на третьей позиции.

    Проверяет что:
      - Число успешно находится в списке
      - Количество попыток соответствует позиции элемента (3)
      - Возвращается корректное найденное число
    """
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result, attempts = guess_number(3, numbers, 'linear')
    self.assertEqual(result, 3)
    self.assertEqual(attempts, 3)

  def test_binary_search_first_element(self):
    """Тест бинарного поиска: поиск первого элемента списка.

    Проверяет что алгоритм корректно находит элемент
    в начале отсортированного списка.
    """
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result, attempts = guess_number(1, numbers, 'binary')
    self.assertEqual(result, 1)
    self.assertGreater(attempts, 0)

  def test_linear_search_last_element(self):
    """Тест линейного поиска: поиск последнего элемента списка.

    Проверяет что:
      - Число успешно находится в конце списка
      - Количество попыток равно длине списка (10)
      - Возвращается корректное найденное число
    """
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result, attempts = guess_number(10, numbers, 'linear')
    self.assertEqual(result, 10)
    self.assertEqual(attempts, 10)

  def test_binary_search_not_found(self):
    """Тест бинарного поиска: число отсутствует в списке.

    Проверяет что:
      - При отсутствии числа выбрасывается ValueError
      - Сообщение об ошибке содержит информацию о ненайденном числе
    """
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    with self.assertRaises(ValueError) as context:
      guess_number(15, numbers, 'binary')
    self.assertIn("Числа 15 нет в списке", str(context.exception))

  def test_linear_search_not_found(self):
    """Тест линейного поиска: число отсутствует в списке.

    Проверяет что:
      - При отсутствии числа выбрасывается ValueError
      - Сообщение об ошибке содержит информацию о ненайденном числе
    """
    numbers = [1, 2, 3, 4, 5]
    with self.assertRaises(ValueError) as context:
      guess_number(8, numbers, 'linear')
    self.assertIn("Число 8 нет в списке", str(context.exception))

  def test_binary_search_unsorted_list(self):
    """Тест бинарного поиска с несортированным списком.

    Проверяет что:
      - Функция корректно работает с несортированным списком
      - Число успешно находится после внутренней сортировки
      - Количество попыток больше нуля
    """
    numbers = [5, 2, 8, 1, 9, 3, 7, 4, 6, 10]
    result, attempts = guess_number(7, numbers, 'binary')
    self.assertEqual(result, 7)
    self.assertGreater(attempts, 0)

  def test_linear_search_unsorted_list(self):
    """Тест линейного поиска с несортированным списком.

    Проверяет что линейный поиск корректно работает
    с несортированными списками и находит элемент независимо от его позиции.
    """
    numbers = [5, 2, 8, 1, 9, 3, 7, 4, 6, 10]
    result, attempts = guess_number(7, numbers, 'linear')
    self.assertEqual(result, 7)
    # В несортированном списке позиция может быть разной

  def test_invalid_method(self):
    """Тест с неверным методом поиска.

    Проверяет что:
      - При передаче некорректного метода выбрасывается ValueError
      - Сообщение об ошибке указывает на допустимые методы
    """
    numbers = [1, 2, 3, 4, 5]
    with self.assertRaises(ValueError) as context:
      guess_number(3, numbers, 'invalid_method')
    self.assertEqual(
      "Метод должен быть 'binary' или 'linear'", str(context.exception))

  def test_empty_list(self):
    """Тест с пустым списком.

    Проверяет что при поиске в пустом списке выбрасывается ValueError
    с соответствующим сообщением об ошибке.
    """
    numbers = []
    with self.assertRaises(ValueError) as context:
      guess_number(5, numbers, 'binary')
    self.assertIn("Числа 5 нет в списке", str(context.exception))

  def test_single_element_binary(self):
    """Тест бинарного поиска с списком из одного элемента.

    Проверяет что:
      - Число успешно находится в списке из одного элемента
      - Количество попыток равно 1
    """
    numbers = [5]
    result, attempts = guess_number(5, numbers, 'binary')
    self.assertEqual(result, 5)
    self.assertEqual(attempts, 1)

  def test_single_element_linear(self):
    """Тест линейного поиска с списком из одного элемента.

    Проверяет что:
      - Число успешно находится в списке из одного элемента
      - Количество попыток равно 1
    """
    numbers = [5]
    result, attempts = guess_number(5, numbers, 'linear')
    self.assertEqual(result, 5)
    self.assertEqual(attempts, 1)


if __name__ == '__main__':
  """Запуск тестового набора.

  Запускает все тесты с детальным выводом (verbosity=2),
  что позволяет видеть подробную информацию о каждом тесте.
  """
  unittest.main(verbosity=2)

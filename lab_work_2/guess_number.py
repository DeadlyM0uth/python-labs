def guess_number(number: int, numbers_list: list[int], method: str) -> tuple[int, int]:
  """Угадывает число из списка с использованием указанного алгоритма поиска.
  
  Args:
    number (int): Число, которое нужно найти в списке
    numbers_list (list[int]): Отсортированный список целых чисел для поиска
    method (str): Метод поиска - 'binary' для бинарного или 'linear' для линейного
  
  Returns:
    tuple[int, int]: Кортеж содержащий:
      - Найденное число
      - Количество попыток, потребовавшихся для поиска

  Raises:
    ValueError: Если передан неподдерживаемый метод поиска
    ValueError: Если число не найдено в списке
  
  Example:
    >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> guess_number(5, numbers, 'binary')
    (5, 3)
    >>> guess_number(5, numbers, 'linear')
    (5, 5)
  """
  if method not in ['binary', 'linear']:
    raise ValueError("Метод должен быть 'binary' или 'linear'")
  
  if method == 'binary':
    return _binary_search(number, numbers_list)
  else:
    return _linear_search(number, numbers_list)

def _linear_search(target: int, numbers: list[int]) -> tuple[int, int]:
  """Выполняет линейный поиск числа в списке.
    
  Проходит по всем элементам списка последовательно до нахождения целевого числа.
  Временная сложность: O(n)
  
  Args:
    target (int): Число для поиска
    numbers (list[int]): Список чисел для поиска (может быть неотсортированным)
  
  Returns:
    tuple[int, int]: Кортеж содержащий:
      - Найденное число
      - Количество итераций (попыток)
  
  Raises:
    ValueError: Если целевое число не найдено в списке
  """
  attempts = 0
  for num in numbers:
    attempts += 1
    if target == num:
      return num, attempts
  
  raise ValueError(f"Число {target} нет в списке")
  
def _binary_search(target: int, numbers: list[int]) -> tuple[int, int]:
  """Выполняет бинарный поиск числа в отсортированном списке.
  
  Делит область поиска пополам на каждой итерации.
  Временная сложность: O(log n)
  
  Args:
    target (int): Число для поиска
    numbers (list[int]): Список чисел для поиска (будет отсортирован)
  
  Returns:
    tuple[int, int]: Кортеж содержащий:
      - Найденное число
      - Количество итераций (попыток)
  
  Raises:
    ValueError: Если целевое число не найдено в списке
  
  Note:
    Функция сортирует переданный список перед выполнением поиска.
    Исходный порядок элементов не сохраняется.
  """
  attempts = 0
  numbers.sort()
  left, right = 0, len(numbers) - 1

  while left <= right:
    attempts += 1
    mid = (left + right) // 2
    guess = numbers[mid]

    if guess == target:
      return guess, attempts
    elif guess < target:
      left = mid + 1
    else:
      right = mid - 1
    
  raise ValueError(f"Числа {target} нет в списке")


def input_helper() -> tuple[int, list[int], str]:
  """Вспомогательная функция для интерактивного ввода данных пользователем.
  
  Запрашивает у пользователя:
    - Диапазон чисел (начало и конец)
    - Число для поиска
    - Метод поиска
  
  Returns:
    tuple[int, list[int], str]: Кортеж содержащий:
      - Целевое число для поиска
      - Сгенерированный список чисел в указанном диапазоне
      - Выбранный метод поиска ('binary' или 'linear')
  
  Note:
    При некорректном вводе функция рекурсивно запрашивает данные повторно.
  """
  print("=== Угадай число ===")
  
  # Ввод диапазона
  try:
    start = int(input("Введите начало диапазона: "))
    end = int(input("Введите конец диапазона: "))
    if start >= end:
      print("Ошибка: начало диапазона должно быть меньше конца")
      return input_helper()
  except ValueError:
      print("Ошибка: введите целые числа")
      return input_helper()
  
  # Ввод числа для угадывания
  try:
    target = int(input("Введите число для угадывания: "))
    if target < start or target > end:
      print(f"Ошибка: число должно быть в диапазоне [{start}, {end}]")
      return input_helper()
  except ValueError:
    print("Ошибка: введите целое число")
    return input_helper()

  # Ввод метода поиска
  method_number = input("Выберите метод поиска (default binary):\n\t1. binary\n\t2. linear\n> ")
  methods = {"1": "binary", "2": "linear"}
  method = methods[method_number] if method_number in methods else "binary"
    
  
  numbers_list = list(range(start, end + 1))
  return target, numbers_list, method


def main():
  """Основная функция для запуска игры в угадывание чисел.
  
  Обрабатывает пользовательский ввод, выполняет поиск и выводит результаты.
  Обрабатывает возможные исключения в процессе выполнения.
  
  Raises:
    KeyboardInterrupt: При прерывании программы пользователем (Ctrl+C)
    Exception: При возникновении непредвиденных ошибок
  """
  try:
    target, numbers_list, method = input_helper()
    result, attempts = guess_number(target, numbers_list, method)
    
    print(f"\nРезультат:")
    print(f"Угаданное число: {result}")
    print(f"Количество попыток: {attempts}")
    print(f"Использованный метод: {method}")
  except ValueError as e:
    print(f"Ошибка: {e}")
  except KeyboardInterrupt:
    print("\nПрограмма прервана пользователем")
  except Exception as e:
    print(f"Неожиданная ошибка: {e}")

if __name__ == "__main__":
  main()
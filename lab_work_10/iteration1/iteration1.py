from typing import Callable

# Итерация 1
def integrate(f: Callable[[float], float], 
            a: float, 
            b: float, 
            *, 
            n_iter: int = 100000) -> float:
  """
  Вычисляет определенный интеграл функции методом прямоугольников.
  
  Args:
    f: Функция одного аргумента, которую нужно интегрировать.
    a: Нижний предел интегрирования.
    b: Верхний предел интегрирования.
    n_iter: Количество итераций (прямоугольников) для вычисления.
           Большее значение дает более точный результат, но требует
           больше времени на вычисление.
  
  Returns:
    Приближенное значение определенного интеграла ∫f(x)dx от a до b.
  
  Examples:
    >>> import math
    >>> round(integrate(math.cos, 0, math.pi, n_iter=10_000), 3)
    0.0
  
    >>> round(integrate(lambda x: x**2, 0, 1, n_iter=10_000), 3)
    0.333
  """
  acc = 0.0
  step = (b - a) / n_iter
  for i in range(n_iter):
    acc += f(a + i * step) * step
  return acc


import doctest


# Запуск doctest
if __name__ == "__main__":
    # Запускаем doctest
    doctest.testmod(verbose=True)
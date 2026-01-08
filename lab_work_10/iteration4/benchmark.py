import integrate_cython as cy
from iteration4 import integrate_cython_processed, integrate_cython_threaded
from iteration1.iteration1 import integrate
from iteration2.iteration2 import integrate_threaded
from iteration3.iteration3 import integrate_processed
import math
import timeit

def benchmark():
  n_iter = 10_000_000
  a,b = 0, math.pi
  
  # 1. Линейная версия на python
  print("\n1. Оригинальная Python версия (однопоточная):")
  time_py = timeit.timeit(
    lambda: integrate(math.sin, a, b, n_iter=n_iter),
    number=1
  )
  print(f"   Время: {time_py:.4f} сек")
  
  # 2. Cython линейная версия
  print("\n2. Cython версия (однопоточная):")
  time_cy = timeit.timeit(
    lambda: cy.integrate_cython(math.sin, a, b, n_iter=n_iter),
    number=1
  )
  print(f"   Время: {time_cy:.4f} сек")
  print(f"   Ускорение: {time_py/time_cy:.2f}x")
  
  
benchmark()
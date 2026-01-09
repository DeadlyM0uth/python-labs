import iteration4.integrate_cython as cy # type: ignore
from iteration4.iteration4 import (
  integrate_cython_processed,
  integrate_cython_threaded,
)
from iteration1.iteration1 import integrate
from iteration2.iteration2 import integrate_threaded
from iteration3.iteration3 import integrate_processed
import math
import timeit

def benchmark():
  n_iter = 10_000_000
  a,b = 0, math.pi
  
  #===1===
  # Линейная версия на python
  print("\n1. Линейная версия:")
  print("\n\tPython:")
  time_py = timeit.timeit(
    lambda: integrate(math.sin, a, b, n_iter=n_iter),
    number=1
  )
  print(f"\tВремя: {time_py:.4f} сек")
  
  # Cython линейная версия
  print("\n\tCython")
  time_cy = timeit.timeit(
    lambda: cy.integrate_cython(math.sin, a, b, n_iter=n_iter),
    number=1
  )
  print(f"\tВремя: {time_cy:.4f} сек")
  print(f"\tУскорение: {time_py/time_cy:.2f}x")
  
  #===2===
  # Многопоточная версия на python
  print("\n2. Многопоточная версия 4 потокоа:")
  print("\n\tPython:")
  time_py = timeit.timeit(
    lambda: integrate_threaded(math.sin, a, b, n_iter=n_iter, n_jobs=4),
    number=1
  )
  print(f"\tВремя: {time_py:.4f} сек")
  
  # Cython многопоточная версия
  print("\n\tCython")
  time_cy = timeit.timeit(
    lambda: integrate_cython_threaded(math.sin, a, b, n_iter=n_iter, n_jobs=4),
    number=1
  )
  print(f"\tВремя: {time_cy:.4f} сек")
  print(f"\tУскорение: {time_py/time_cy:.2f}x")
  
  #===3===
  # Многопроцессорная версия на python
  print("\n3. Многопроцессорная версия 4 работника:")
  print("\n\tPython:")
  time_py = timeit.timeit(
    lambda: integrate_processed(math.sin, a, b, n_iter=n_iter, n_jobs=4),
    number=1
  )
  print(f"\tВремя: {time_py:.4f} сек")
  
  # Cython многопроцессорная версия
  print("\n\tCython")
  time_cy = timeit.timeit(
    lambda: integrate_cython_processed(math.sin, a, b, n_iter=n_iter, n_jobs=4),
    number=1
  )
  print(f"\tВремя: {time_cy:.4f} сек")
  print(f"\tУскорение: {time_py/time_cy:.2f}x")


if __name__ == "__main__":
  benchmark()
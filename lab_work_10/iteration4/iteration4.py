import math
import concurrent.futures as ftres
from iteration1.iteration1 import integrate
from functools import partial
import integrate_cython as cy

# Многопоточная версия с Cython
def integrate_cython_threaded(
  f, 
  a: float, 
  b: float, 
  *, 
  n_jobs: int = 2, 
  n_iter: int = 10000
  ) -> float:
  """
  Многопоточная версия с Cython-оптимизированной функцией.
  """
  executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)
  
  spawn = partial(executor.submit, cy.integrate_cython, f, 
                  n_iter=n_iter // n_jobs)
  
  step = (b - a) / n_jobs
  fs = []
  
  for i in range(n_jobs):
    a_i = a + i * step
    b_i = a + (i + 1) * step
    fs.append(spawn(a_i, b_i))
  
  results = [f.result() for f in ftres.as_completed(fs)]
  return sum(results)
  
  
# Многопроцессная версия с Cython
def integrate_cython_processed(
  f, 
  a: float, 
  b: float, 
  *, 
  n_jobs: int = 2, 
  n_iter: int = 10001
  ) -> float:
  """
  Многопроцессная версия с Cython-оптимизированной функцией.
  """
  executor = ftres.ProcessPoolExecutor(max_workers=n_jobs)
  
  spawn = partial(executor.submit, cy.integrate_cython, f, 
                  n_iter=n_iter // n_jobs)
  
  step = (b - a) / n_jobs
  fs = []
  
  for i in range(n_jobs):
    a_i = a + i * step
    b_i = a + (i + 1) * step
    fs.append(spawn(a_i, b_i))
  
  results = [f.result() for f in ftres.as_completed(fs)]
  return sum(results)


a = integrate_cython_threaded(math.sin, 0, math.pi, 2, 10000)
print(a)
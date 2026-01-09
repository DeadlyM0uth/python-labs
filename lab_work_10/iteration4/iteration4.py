import concurrent.futures as ftres
from functools import partial
import iteration4.integrate_cython as cy # type: ignore

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



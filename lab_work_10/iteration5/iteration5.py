import iteration5.integrate_nogil as ng # type: ignore
import concurrent.futures as ftres
from functools import partial

def integrate_nogil_threaded_sin(
  a: float,
  b: float,
  *,
  n_jobs: int = 2,
  n_iter: int = 10000
  ) -> float:
  """
  Многопоточная nogil версия интеграции синуса
  """
  executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)
  spawn = partial(executor.submit, ng.integrate_nogil_sin, n_iter=n_iter // n_jobs)
  step = (b - a) / n_jobs
  fs = []
  
  
  for i in range(n_jobs):
    a_i = a + i *step
    b_i = a + (i+1) * step
    fs.append(spawn(a_i, b_i))
    results = [f.result() for f in ftres.as_completed(fs)]
  return sum(results)
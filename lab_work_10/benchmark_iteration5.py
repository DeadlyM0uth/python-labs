from iteration4.iteration4 import integrate_cython_processed
# from iteration5.iteration5 import integrate_nogil_threaded_sin
from iteration5.integrate_nogil import integrate_sin_nogil_threads # type: ignore
import math
import timeit

def benchmark():
  n_iter = 10_000_000
  a,b = 0, math.pi

  print("\nБенчмарк многопоточной noGIL версии (sin от 0 до π, n_iter=10_000_000):")
  for n_jobs in [2, 4, 6, 8]:
    time = timeit.timeit( 
      lambda: integrate_sin_nogil_threads(0, math.pi, 
        n_jobs=n_jobs, n_iter=n_iter),
      number=1
    )
    print(f"n_jobs={n_jobs}: {time:.6f} ") 
    
  print("\nБенчмарк многопроцессороной Cyhton версии (sin от 0 до π, n_iter=10_000_000):")
  for n_jobs in [1, 2, 4, 6, 8]:
    time = timeit.timeit( 
      lambda: integrate_cython_processed(math.sin, 0, math.pi, 
        n_jobs=n_jobs, n_iter=n_iter),
      number=1
    )
    print(f"n_jobs={n_jobs}: {time:.6f} ") 
    

if __name__ == "__main__":
  benchmark()
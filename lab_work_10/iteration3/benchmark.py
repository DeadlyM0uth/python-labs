from iteration3 import integrate_processed
import math
import timeit

def benchmark_processed():
    print("\nБенчмарк многопроцессорной версии (sin от 0 до π, n_iter=1_000_000):")
    
    for n_jobs in [1, 2, 4, 6, 8]:
        time = timeit.timeit( 
          lambda: integrate_processed(math.sin, 0, math.pi, 
            n_jobs=n_jobs, n_iter=1_000_000),
          number=1
        )
        
        print(f"n_jobs={n_jobs}: {time:.6f} секунд на одно выполнение")


if __name__ == "__main__":
  benchmark_processed()
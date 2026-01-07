import time
import math
from iteration2.iteration2 import integrate_threaded
from iteration3.iteration3 import integrate_processed

def compare_threads_processes():
    print("\nСравнение потоков и процессов (sin от 0 до π, n_iter=1000000):")
    print("-" * 60)
    
    for n_jobs in [2, 4, 6, 8]:
        # Многопоточность
        start_time = time.time()
        result_t = integrate_threaded(math.sin, 0, math.pi, 
                                      n_jobs=n_jobs, n_iter=10_000_000)
        time_t = time.time() - start_time
        
        # Многопроцессность
        start_time = time.time()
        result_p = integrate_processed(math.sin, 0, math.pi, 
                                       n_jobs=n_jobs, n_iter=10_000_000)
        time_p = time.time() - start_time
        
        print(f"Работников: {n_jobs}")
        print(f"  Потоки:    {result_t:.6f}, время: {time_t:.4f} сек")
        print(f"  Процессы:  {result_p:.6f}, время: {time_p:.4f} сек")
        print(f"  Ускорение: {time_t/time_p:.2f}x")
        print("-" * 60)
        
        
if __name__ == "__main__":
  compare_threads_processes()
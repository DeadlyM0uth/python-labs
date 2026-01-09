import math
import timeit
from iteration1.iteration1 import integrate

# Замер времени выполнения для разных чисел итераций
def measure_performance():
    print("Замер времени выполнения для функции math.sin от 0 до π:")
    for n in [100, 1000, 10000, 100000, 1000000]:
        time = timeit.timeit(
            lambda: integrate(math.sin, 0, math.pi, n_iter=n),
            number=10
        )
        print(f"n_iter={n:8d}: {time/10:.6f} секунд на одно выполнение")
 
if __name__ == "__main__":
  measure_performance()
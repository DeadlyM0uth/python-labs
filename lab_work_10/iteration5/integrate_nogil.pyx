import cython
from libc.math cimport sin

from cython.parallel import prange, parallel

ctypedef double (*func_t)(double) nogil

# Nogil версия вычислительной части
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
def integrate_sin_threaded(double a, double b, long n_iter, int n_threads=0):
    """
    Вычисляет интеграл sin(x) от a до b методом прямоугольников с использованием prange.
    
    Parameters:
    -----------
    a, b : float
        Пределы интегрирования
    n_points : int
        Количество точек разбиения
    num_threads : int
        Количество потоков (0 = автоопределение)
    """
    cdef:
        double dx = (b - a) / n_iter
        double total = 0.0
        long i
        double x
    
    # Параллельный цикл с reduction
    with nogil:
        for i in prange(n_iter, num_threads=n_threads, schedule='static'):
            x = a + (i + 0.5) * dx
            total += sin(x)
    
    return total * dx
import cython
from libc.math cimport sin, cos

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
cpdef double integrate_cython(f, double a, double b, int n_iter=100000):
    """
    Cython-оптимизированная версия численного интегрирования методом прямоугольников.
    
    Args:
        f: Функция Python или C-функция
        a: Нижний предел
        b: Верхний предел
        n_iter: Количество итераций
    
    Returns:
        Приближенное значение интеграла
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef double x
    cdef int i
    
    for i in range(n_iter):
        x = a + i * step
        acc += f(x) * step
    
    return acc

# integrate_cython.pyx
import cython
from libc.math cimport cos, sin

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef double integrate_cython(object f, double a, double b, int n_iter=100000):

    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef double x
    cdef int i

    # `f` is a Python callable; cast the result to double for arithmetic
    for i in range(n_iter):
            x = a + i * step
            acc += <double>f(x) * step

    return acc

# Функции для тестирования
cpdef double my_sin(double x):
    return sin(x)

cpdef double my_cos(double x):
    return cos(x)

cpdef double square(double x):
    return x * x
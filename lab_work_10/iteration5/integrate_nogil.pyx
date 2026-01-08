import cython
from libc.math cimport sin as c_sin

from cython.parallel import prange, parallel

ctypedef double (*func_t)(double) nogil

# Nogil версия вычислительной части
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
cdef double integrate_nogil(func_t f, double a, double b, int n_iter) nogil:
  """
  Вычислительная часть интеграции без GIL.
  """
  cdef double acc = 0.0
  cdef double step = (b - a) / n_iter
  cdef double x
  cdef int i
  
  for i in range(n_iter):
    x = a + i * step
    acc += f(x) * step
  
  return acc

def integrate_sin_nogil_threads(double a, double b, int n_jobs=2, int n_iter=10_000_000):
  cdef double step_chunk = (b - a) / n_jobs
  cdef double[64] results
  cdef int i
  cdef double total = 0.0
  cdef int iter_per_chunk = n_iter // n_jobs

  with nogil:
    for i in prange(n_jobs, num_threads=n_jobs, schedule='static'):
      results[i] = integrate_nogil(c_sin, a + i * step_chunk, a + (i + 1) * step_chunk, iter_per_chunk)

  for i in range(n_jobs):
    total += results[i]
  return total
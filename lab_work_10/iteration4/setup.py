# setup.py
from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize("iteration4.pyx", 
                         annotate=True),  # Генерируем HTML с аннотациями
    include_dirs=[numpy.get_include()]
)
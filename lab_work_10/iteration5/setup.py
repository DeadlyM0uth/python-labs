from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np
import platform
import sys

# Определяем флаги компиляции для Windows
if platform.system() == "Windows":
    compile_args = ['/openmp', '/O2', '/fp:fast']
    link_args = []
    libraries = []
else:
    # Флаги для Linux/Mac
    compile_args = ['-fopenmp', '-O3', '-march=native', '-ffast-math']
    link_args = ['-fopenmp']
    libraries = ['m']

extensions = [
    Extension(
        "integrate_nogil",
        sources=["integrate_nogil.pyx"],
        include_dirs=[np.get_include()],
        libraries=libraries,
        extra_compile_args=compile_args,
        extra_link_args=link_args,
        language="c"
    )
]

setup(
    name="integrate_nogil",
    ext_modules=cythonize(extensions, compiler_directives={
        'language_level': "3",
        'boundscheck': False,
        'wraparound': False,
        'initializedcheck': False,
        'cdivision': True,
    }),
    include_dirs=[np.get_include()]
)
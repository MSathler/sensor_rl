from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("cython_for.pyx"))
setup(ext_modules=cythonize("cython_pc.pyx"))


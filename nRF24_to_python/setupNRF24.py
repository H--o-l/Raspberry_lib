from distutils.core import setup, Extension
import os

os.environ["CC"] = "g++"

# the c++ extension module
extension_mod = Extension('nRF24ForPython',
                          language = "c++",
                          include_dirs = ['/home/pi/rf24libs/RF24'],
                          libraries = ['rf24-bcm','rt'],
                          sources = ['nRF24ForPython.c',
                                     'nRF24.c'])

setup(name = "nRF24ForPython", ext_modules=[extension_mod])

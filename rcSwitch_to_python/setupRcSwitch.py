from distutils.core import setup, Extension
import os

os.environ["CC"] = "g++"

# the c++ extension module
extension_mod = Extension('rcSwitchForPython',
                          language = "c++",
                          include_dirs = ['/home/pi/rcswitch-pi'],
                          libraries = ['wiringPi', 'wiringPiDev'],
                          sources = ['rcSwitchForPython.c',
                                     '/home/pi/rcswitch-pi/RCSwitch.cpp'])


setup(name = "rcSwitchForPython", ext_modules=[extension_mod])

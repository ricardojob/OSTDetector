import sys as sos
from math import cos, pi
import unittest
from unittest import mock

temp_plat = sos.platform
@unittest.skipIf(condition= temp_plat == 'mac', reason='exemplos decorator list')
def m1():
    print(temp_plat)

@unittest.skipIf(condition= sos.platform == 'linux', reason='exemplos simples')
def m2():
    print('cos(pi) is', cos(pi))
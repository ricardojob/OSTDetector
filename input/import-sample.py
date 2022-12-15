# arquivo com exemplos de imports
import sys as sos
from math import sin as seno
import unittest
from unittest import mock

temp_plat = sos.platform
@unittest.skipIf(condition= sos.platform == 'mac', reason='exemplos decorator list')
def m1():
    print(temp_plat)
    print('sen(1): ', seno(1))

@unittest.skipIf(condition= temp_plat == 'linux', reason='exemplos simples')
def m2():
    from math import cos, pi
    print('cos(pi): ', cos(pi))
    print(sos.version)
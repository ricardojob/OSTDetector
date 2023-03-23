import sys
import platform
import os
from unittest import skipIf
import pytest

# treat
if platform.system() == 'Linux':
    pass
# if not os.name != 'nt':
#     pass
if sys.platform.startswith('win'):
    pass

# @pytest.mark.skipif(os.name != "nt", reason="Test only on Windows")
# def test_should_bypass_proxies_win_registry_bad_values(monkeypatch): # requests (/tests/test_utils.py, line 867)
#     pass

# # skip
if sys.platform != 'Darwin':
    pass
# if not platform.system() == 'AIX':
#     pass
if not sys.platform.endswith('BSD'): #algoritmo ainda não funciona para capturar o parametro
    pass

# @skipIf(sys.platform == "win32", "Windows uses non-standard time zone names")
# def test_tz_template_context_processor(self):  #django (/tests/timezones/tests.py, line 1243)
#     pass

# @pytest.mark.skipif(sys.platform.startswith('darwin'), reason='macOS requires passlib')
# def test_encrypt_with_rounds_no_passlib(): #ansible (/test/units/utils/test_encrypt.py, line 40)
#     pass

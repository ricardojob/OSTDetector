import sys
import platform
import pytest
import os as sos
dwith_mp = sys.platform 
with_mp = sys.platform not in ['win32']
num_workers_list = [0, 2] if with_mp else [0]

if any(sys.platform): pass
if sos.name != 'a': pass
if platform.platform: pass

not any([x for x in ["ubuntu", "debian"] if x in platform.platform()])

@pytest.mark.skipif(
    not any([x for x in ["ubuntu", "debian"] if x in platform.platform()]),
    reason="Test only for debian based platforms",
)
def test_adding_repo_file():
    pass
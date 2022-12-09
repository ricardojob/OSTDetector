# contents of runpytest.py
# https://github.com/pytest-dev/pytest/discussions/2039
import pytest

class CollectPlugin:
    def __init__(self):
        self.collected = []

    def pytest_collection_modifyitems(self, session, config, items):
        for item in items:
            # https://docs.pytest.org/en/stable/reference/reference.html#pytest.Item
            self.collected.append(item.nodeid)
            # print(item.path)
        # https://docs.pytest.org/en/stable/reference/reference.html#pytest.Session
        print('session: ', session.name)
        # https://docs.pytest.org/en/stable/reference/reference.html#pytest.Config
        print('config: ', config.rootpath)

plugin = CollectPlugin()
pytest.main(['--collect-only'], plugins=[plugin])
for nodeid in plugin.collected:
    print(nodeid)


# plugin = CollectPlugin()
# dir = '/Users/job/Documents/dev/doutorado/study/skip-platform/input'
# file_python = '../input/pytest-sample.py'
# file_python = '../input'
# --rootdir=/Users/job/Documents/dev/doutorado/study/skip-platform/input
# pytest.skip(allow_module_level=True)
# pytest.main(['--collect-only'], plugins=[plugin])
# pytest.main(['--continue-on-collection-errors'], plugins=[plugin])
# pytest.main(['--collect-only', '--rootdir=./input'], plugins=[plugin])
# pytest.main(['--collect-only', file_python], plugins=[plugin])
# pytest.main(['--collect-only', '-p', 'no:terminal', directory], plugins=[plugin])

# for nodeid in plugin.collected:
#     print(nodeid)
# --continue-on-collection-errors

# https://stackoverflow.com/questions/73469467/pytest-collect-all-tests-name-before-running-test
# @pytest.fixture(scope='session', autouse=True)
# def make_test_outputs_folders():
    # coll = TestCollection()
    # directory = sys.argv[1]
    # pytest.main(['--collect-only', directory], plugins=[coll])
    # for case in coll.collected:
    #     os.makedirs(os.path.join('tmp', case.replace("::", ".")), exist_ok=True)
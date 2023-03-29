verificandoatribuição às variáveis

<!-- data1/sanic/tests/test_logo.py
def test_get_logo_returns_no_colors_on_apple_terminal():
    platform = sys.platform
    sys.platform = "darwin"
    os.environ["TERM_PROGRAM"] = "Apple_Terminal"
    with patch("sys.stdout.isatty") as isatty:
        isatty.return_value = False
        logo = get_logo()
    assert "\033" not in logo
    sys.platform = platform
    del os.environ["TERM_PROGRAM"] 
-->

<!-- data1/ansible/ansible/ansible/test/lib/ansible_test/_internal/commands/env/__init__.py
platform=dict(
    datetime=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    platform=platform.platform(),
    uname=platform.uname(),
), 
-->

<!-- data1/django/django/django/django/core/management/utils.py

p = run(args, capture_output=True, close_fds=os.name != "nt") 
-->


<!-- data1/sanic/tests/test_logo.py
def test_get_logo_returns_no_colors_on_apple_terminal():
    platform = sys.platform
    sys.platform = "darwin"
    os.environ["TERM_PROGRAM"] = "Apple_Terminal"
    with patch("sys.stdout.isatty") as isatty:
        isatty.return_value = False
        logo = get_logo()
    assert "\033" not in logo
    sys.platform = platform
    del os.environ["TERM_PROGRAM"] -->

<!-- 
    https://github.com/keras-team/keras/blob/b661c9f73d8860cda6425e3c5b0b1ec145329dc1/keras/legacy_tf_layers/core_test.py#L631 
-->

<!-- https://github.com/pyg-team/pytorch_geometric/blob/743c1c1d9a33072ed80082ddb31f4be1080e0233/test/loader/test_dataloader.py#L12
with_mp = sys.platform not in ['win32']
num_workers_list = [0, 2] if with_mp else [0] 
-->

Bugg a tratar

```python

if any(platform.win32_ver()):
 pass

assert sys.platform.startswith("linux") is False, "This test can't run under linux"

any([x for x in ["ubuntu", "debian"] if x in platform.platform()])

with_mp = sys.platform not in ['win32']
num_workers_list = [0, 2] if with_mp else [0]

```


## importante
https://docs.pytest.org/en/7.2.x/example/markers.html#marking-platform-specific-tests-with-pytest

pytest tenta diminuir o problema com testes flaky

https://docs.pytest.org/en/7.2.x/explanation/flaky.html 


## pytest decorators


```
 pytest --markers
@pytest.mark.webtest: mark a test as a webtest.

@pytest.mark.slow: mark test as slow.

@pytest.mark.filterwarnings(warning): add a warning filter to the given test. see https://docs.pytest.org/en/stable/how-to/capture-warnings.html#pytest-mark-filterwarnings

@pytest.mark.skip(reason=None): skip the given test function with an optional reason. Example: skip(reason="no way of currently testing this") skips the test.

@pytest.mark.skipif(condition, ..., *, reason=...): skip the given test function if any of the conditions evaluate to True. Example: skipif(sys.platform == 'win32') skips the test if we are on the win32 platform. See https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-skipif

@pytest.mark.xfail(condition, ..., *, reason=..., run=True, raises=None, strict=xfail_strict): mark the test function as an expected failure if any of the conditions evaluate to True. Optionally specify a reason for better reporting and run=False if you don't even want to execute the test function. If only specific exception(s) are expected, you can list them in raises, and if the test fails in other ways, it will be reported as a true failure. See https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-xfail

@pytest.mark.parametrize(argnames, argvalues): call a test function multiple times passing in different arguments in turn. argvalues generally needs to be a list of values if argnames specifies only one name or a list of tuples of values if argnames specifies multiple names. Example: @parametrize('arg1', [1,2]) would lead to two calls of the decorated test function, one with arg1=1 and another with arg1=2.see https://docs.pytest.org/en/stable/how-to/parametrize.html for more info and examples.

@pytest.mark.usefixtures(fixturename1, fixturename2, ...): mark tests as needing all of the specified fixtures. see https://docs.pytest.org/en/stable/explanation/fixtures.html#usefixtures

@pytest.mark.tryfirst: mark a hook implementation function such that the plugin machinery will try to call it first/as early as possible. DEPRECATED, use @pytest.hookimpl(tryfirst=True) instead.

@pytest.mark.trylast: mark a hook implementation function such that the plugin machinery will try to call it last/as late as possible. DEPRECATED, use @pytest.hookimpl(trylast=True) instead.

```

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

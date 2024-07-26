# https://github.com/Vivrish/Arkly_site/blob/fec40e05594a75f60cd3d70ba199f84fc3c7883d/django/tests/shell/tests.py
import sys
import unittest

@unittest.skipIf(sys.platform == 'macos',"Mac supports file descriptors.",)
class ShellCommandTestCase(SimpleTestCase):

    @unittest.skipIf(sys.platform == 'win32',"Linux is better",)
    def test_function(self, select):
        with captured_stdin() as stdin, captured_stdout() as stdout:
            stdin.write(self.script_globals)
            stdin.seek(0)
            call_command('shell')
        self.assertEqual(stdout.getvalue().strip(), 'True')

    @unittest.skipIf(sys.platform == 'linux',"Windows select() doesn't support file descriptors.",)
    async def test_function_async(self, select):
        with captured_stdin() as stdin, captured_stdout() as stdout:
            stdin.write(self.script_with_inline_function)
        self.assertEqual(stdout.getvalue().strip(), __version__)

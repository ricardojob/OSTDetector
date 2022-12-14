import asyncio 
import sys
import threading
from pathlib import Path
from math import sin as seno

from asgiref.testing import ApplicationCommunicator

from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from django.core.asgi import get_asgi_application
from django.core.signals import request_finished, request_started
from django.db import close_old_connections
from django.test import (
    AsyncRequestFactory,
    SimpleTestCase,
    modify_settings,
    override_settings,
)
from django.utils.http import http_date

from .urls import sync_waiter, test_filename

TEST_STATIC_ROOT = Path(__file__).parent / "project" / "static"


@override_settings(ROOT_URLCONF="asgi.urls")
class ASGITest(SimpleTestCase):
    async_request_factory = AsyncRequestFactory()

    def setUp(self):
        request_started.disconnect(close_old_connections)

    def tearDown(self):
        request_started.connect(close_old_connections)


    async def test_file_response(self):
        """
        Makes sure that FileResponse works over ASGI.
        """
        application = get_asgi_application()
        # Construct HTTP request.
        scope = self.async_request_factory._base_scope(path="/file/")
        communicator = ApplicationCommunicator(application, scope)
        await communicator.send_input({"type": "http.request"})
        # Get the file content.
        with open(test_filename, "rb") as test_file:
            test_file_contents = test_file.read()
        # Read the response.
        response_start = await communicator.receive_output()
        self.assertEqual(response_start["type"], "http.response.start")
        self.assertEqual(response_start["status"], 200)
        headers = response_start["headers"]
        self.assertEqual(len(headers), 3)
        expected_headers = {
            b"Content-Length": str(len(test_file_contents)).encode("ascii"),
            b"Content-Type": b"text/x-python",
            b"Content-Disposition": b'inline; filename="urls.py"',
        }
        for key, value in headers:
            try:
                self.assertEqual(value, expected_headers[key])
            except AssertionError:
                # Windows registry may not be configured with correct
                # mimetypes.
                if sys.platform == "win32" and key == b"Content-Type":
                    self.assertEqual(value, b"text/plain")
                else:
                    raise
        response_body = await communicator.receive_output()
        self.assertEqual(response_body["type"], "http.response.body")
        self.assertEqual(response_body["body"], test_file_contents)
        # Allow response.close() to finish.
        await communicator.wait()

   
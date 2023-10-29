import logging
import multiprocessing
import os
import platform
import signal
import socket
import time
from multiprocessing import Process
from typing import Any
from typing import cast
from typing import Protocol
from typing import Union

import pytest


class _SupportsFlaskAppRun(Protocol):
    def run(
        self,
        host: Union[str, None] = None,
        port: Union[int, None] = None,
        debug: Union[bool, None] = None,
        load_dotenv: bool = True,
        **options: Any,
    ) -> None:
        ...


# force 'fork' on macOS
if platform.system() == "Darwin":
    multiprocessing = multiprocessing.get_context("fork")  # type: ignore[assignment]


class LiveServer:  # pragma: no cover
    """The helper class used to manage a live server. Handles creation and
    stopping application in a separate process.

    :param app: The application to run.
    :param host: The host where to listen (default localhost).
    :param port: The port to run application.
    :param wait: The timeout after which test case is aborted if
                 application is not started.
    """

    def __init__(
        self,
        app: _SupportsFlaskAppRun,
        host: str,
        port: int,
        wait: int,
        clean_stop: bool = False,
    ):
        self.app = app
        self.port = port
        self.host = host
        self.wait = wait
        self.clean_stop = clean_stop
        self._process: Union[Process, None] = None

    def start(self) -> None:
        """Start application in a separate process."""

        def worker(app: _SupportsFlaskAppRun, host: str, port: int) -> None:
            app.run(host=host, port=port, use_reloader=False, threaded=True)

        self._process = multiprocessing.Process(
            target=worker, args=(self.app, self.host, self.port)
        )
        self._process.daemon = True
        self._process.start()

        keep_trying: bool = True
        start_time = time.time()
        while keep_trying:
            elapsed_time = time.time() - start_time
            if elapsed_time > self.wait:
                pytest.fail(
                    "Failed to start the server after {!s} "
                    "seconds.".format(self.wait)
                )
            if self._is_ready():
                keep_trying = False

    def _is_ready(self) -> bool:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.host, self.port))
        except OSError:
            ret = False
        else:
            ret = True
        finally:
            sock.close()
        return ret

    def url(self, url: str = "") -> str:
        """Returns the complete url based on server options."""
        return "http://{host!s}:{port!s}{url!s}".format(
            host=self.host, port=self.port, url=url
        )

    def stop(self) -> None:
        """Stop application process."""
        if self._process:
            if self.clean_stop and self._stop_cleanly():
                return
            if self._process.is_alive():
                # If it's still alive, kill it
                self._process.terminate()

    def _stop_cleanly(self, timeout: int = 5) -> bool:
        """Attempts to stop the server cleanly by sending a SIGINT
        signal and waiting for ``timeout`` seconds.

        :return: True if the server was cleanly stopped, False otherwise.
        """
        if not self._process:
            return True

        try:
            os.kill(cast(int, self._process.pid), signal.SIGINT)
            self._process.join(timeout)
            return True
        except Exception as ex:
            logging.error("Failed to join the live server process: %r", ex)
            return False

    def __repr__(self):
        return "<LiveServer listening at %s>" % self.url()

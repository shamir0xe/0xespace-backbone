import subprocess
import logging
from pylib_0xe.config.config import Config

LOGGER = logging.getLogger(__name__)


class EmailFacade:
    def send(self, email: str, title: str, body: str):
        """
        Sends an email via subprocess.

        Raises:
            Exception: If the subprocess call fails or times out.
        """
        command = Config.read_env("email.send-command")
        command = command.format(email=email)
        command = command.format(title=title)
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            shell=True,
        )
        try:
            stdout, stderr = process.communicate(
                input=body, timeout=Config.read_env("email.timeout")
            )
            if process.returncode != 0:
                raise Exception(f"Error sending email: {stderr.strip()}")
        except Exception:
            # TODO: Add something for error
            return
        LOGGER.info(f"err: {stderr}")
        LOGGER.info(f"out: {stdout}")

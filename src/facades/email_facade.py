import subprocess
import logging
from pylib_0xe.config.config import Config

from src.orchestrators.readers.template_reader import TemplateReader
from src.types.email_templates import EmailTemplates
from src.types.exception_types import ExceptionTypes

LOGGER = logging.getLogger(__name__)


class EmailFacade:
    def send(self, email: str, title: str, body: str):
        """
        Sends an email via subprocess.

        Raises:
            Exception: If the subprocess call fails or times out.
        """
        command = Config.read_env("email.send-command")
        command = command.replace("{email}", email)
        command = command.replace("{title}", title)
        LOGGER.info(f"body is:\n{body}")
        LOGGER.info(f"Executing this: {command}")

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            shell=True,
        )
        stderr, stdout = "", ""
        try:
            stdout, stderr = process.communicate(
                input=body, timeout=Config.read_env("email.timeout")
            )
            if process.returncode != 0:
                raise Exception(f"Error sending email: {stderr.strip()}")
        except subprocess.TimeoutExpired:
            process.kill()
            LOGGER.error("Email sending process timed out")
        except Exception as e:
            LOGGER.error(f"Failed to send email: {e}")

        LOGGER.info(f"err: {stderr}")
        LOGGER.info(f"out: {stdout}")

    def create_template(self, email_template: EmailTemplates, **kwargs) -> str:
        body = ""
        if email_template is EmailTemplates.VERIFICATION:
            if not ("code" in kwargs and "user_id" in kwargs and "username" in kwargs):
                raise Exception(ExceptionTypes.ARGUMENTS_INVALID)
            code = kwargs["code"]
            user_id = kwargs["user_id"]
            username = kwargs["username"]
            validating_hash = "#"

            body = TemplateReader.read("email.verification_template", "html")
            body = body.replace("{code}", code)
            body = body.replace("{user_id}", user_id)
            body = body.replace("{username}", username)
            body = body.replace("{validating_hash}", validating_hash)
            LOGGER.info(body)
        else:
            raise Exception(ExceptionTypes.EMAIL_TEMPLATE_INVALID)
        return body

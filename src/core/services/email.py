from typing import List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import DirectoryPath

from core.classes.settings import settings

MAIL_USERNAME = settings.MAIL_USERNAME
MAIL_PASSWORD = settings.MAIL_PASSWORD
MAIL_FROM = settings.MAIL_FROM
MAIL_PORT = settings.MAIL_PORT
MAIL_SERVER = settings.MAIL_SERVER


class EmailService:
    def __init__(
        self,
        user_name: str,
        password: str,
        mail_from: str,
        mail_port: int,
        mail_server: str,
        template_folder: DirectoryPath,
        mail_start_tls: bool = True,
        mail_ssl_tsl: bool = False,
        use_credentials: bool = True,
        validate_certs: bool = True,
    ):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=user_name,
            MAIL_PASSWORD=password,
            MAIL_FROM=mail_from,
            MAIL_PORT=mail_port,
            MAIL_SERVER=mail_server,
            MAIL_STARTTLS=mail_start_tls,
            MAIL_SSL_TLS=mail_ssl_tsl,
            USE_CREDENTIALS=use_credentials,
            VALIDATE_CERTS=validate_certs,
            TEMPLATE_FOLDER=template_folder,
        )

    async def send_email(
        self,
        subject: str,
        recipient: List,
        message: dict,
        template_name: str,
    ):
        msg = MessageSchema(
            subject=subject,
            recipients=recipient,
            template_body=message,
            subtype=MessageType.html,
        )

        fm = FastMail(self.conf)
        await fm.send_message(msg, template_name)

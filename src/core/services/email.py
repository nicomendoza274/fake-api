from dataclasses import dataclass

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import DirectoryPath, SecretStr


@dataclass
class EmailService:
    user_name: str
    password: str
    mail_from: str
    mail_port: int
    mail_server: str
    template_folder: DirectoryPath
    mail_start_tls: bool = True
    mail_ssl_tsl: bool = False
    use_credentials: bool = True
    validate_certs: bool = True

    def get_config(self) -> ConnectionConfig:
        conf = ConnectionConfig(
            MAIL_USERNAME=self.user_name,
            MAIL_PASSWORD=SecretStr(self.password),
            MAIL_FROM=self.mail_from,
            MAIL_PORT=self.mail_port,
            MAIL_SERVER=self.mail_server,
            MAIL_STARTTLS=self.mail_start_tls,
            MAIL_SSL_TLS=self.mail_ssl_tsl,
            USE_CREDENTIALS=self.use_credentials,
            VALIDATE_CERTS=self.validate_certs,
            TEMPLATE_FOLDER=self.template_folder,
        )
        return conf

    async def send_email(
        self,
        subject: str,
        recipient: list,
        message: dict,
        template_name: str,
    ) -> None:
        msg = MessageSchema(
            subject=subject,
            recipients=recipient,
            template_body=message,
            subtype=MessageType.html,
        )

        fm = FastMail(self.get_config())
        await fm.send_message(msg, template_name)

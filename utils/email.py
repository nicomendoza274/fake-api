import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

load_dotenv()

DEFAULT_PORT: int = 587

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = os.getenv("MAIL_PORT", DEFAULT_PORT)
MAIL_SERVER = os.getenv("MAIL_SERVER")


conf = ConnectionConfig(
    MAIL_USERNAME=str(MAIL_USERNAME),
    MAIL_PASSWORD=str(MAIL_PASSWORD),
    MAIL_FROM=str(MAIL_FROM),
    MAIL_PORT=int(MAIL_PORT),
    MAIL_SERVER=str(MAIL_SERVER),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
)


async def send_email(subject: str, recipient: List, message: dict):
    msg = MessageSchema(
        subject=subject,
        recipients=recipient,
        template_body=message,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(msg, template_name="body.html")

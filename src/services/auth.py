import random
from datetime import datetime
from pathlib import Path
from typing import cast

from fastapi import status
from sqlmodel import func, select, text

from core.classes.handle_exception import HandleException
from core.constants.generic_errors import GEN_2002, GEN_4000
from core.database.database import SessionDep
from core.models.email import EmailMessage
from core.services.email import (
    MAIL_FROM,
    MAIL_PASSWORD,
    MAIL_PORT,
    MAIL_SERVER,
    MAIL_USERNAME,
    EmailService,
)
from core.utils.encrypt import create_token
from models.user import (
    User,
    UserCheckCodeDTO,
    UserForgotPasswordDTO,
    UserJWT,
    UserLoggedDTO,
    UserLoginDTO,
    UserResetPasswordDTO,
)
from models.user_code import UserCode


class AuthService:
    def __init__(self, session: SessionDep, user: User | None):
        self.session = session
        self.current_user = user

    async def forgot_password(self, user: UserForgotPasswordDTO) -> None:
        result = self.session.exec(select(User).where(User.email == user.email)).first()
        if not result:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        code = random.randint(100000, 999999)

        user_Code = UserCode(user_code_id=None, user_id=result.user_id, code=code)

        # Send Email
        subject = "Fake API - Change Password"
        full_name = f"{result.first_name} {result.last_name}"
        recipient = [user.email]
        message = EmailMessage(full_name=full_name, code=code).model_dump()

        TEMPLATE_FOLDER = Path(__file__).parent.parent / "templates"
        TEMPLATE_NAME = "forgot.html"

        try:
            # Send Email
            await EmailService(
                MAIL_USERNAME,
                MAIL_PASSWORD,
                MAIL_FROM,
                MAIL_PORT,
                MAIL_SERVER,
                TEMPLATE_FOLDER,
            ).send_email(subject, recipient, message, TEMPLATE_NAME)
        except:
            print("Error to sent mail")

        self.session.add(user_Code)
        self.session.commit()
        self.session.refresh(user_Code)
        return

    def check_code(self, user: UserCheckCodeDTO) -> None:
        statement = (
            select(UserCode)
            .join(User, UserCode.user_id == User.user_id)  # type: ignore
            .where(
                UserCode.deleted_at == None,
                UserCode.created_at > func.now() - text("INTERVAL '1 hour'"),
                UserCode.code == user.recovery_code,
                User.email == user.email,
            )
        )
        result = self.session.exec(statement).first()

        if not result:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        result.deleted_at = cast(datetime, func.now())

        self.session.commit()
        self.session.refresh(result)
        return

    def reset_password(self, user: UserResetPasswordDTO) -> None:
        statement = (
            select(User)
            .join(UserCode, UserCode.user_id == User.user_id)  # type: ignore
            .where(
                UserCode.code == user.recovery_code,
                User.email == user.email,
            )
        )
        result = self.session.exec(statement).first()

        if not result:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        result.hash = user.hash if user.hash else ""

        self.session.commit()
        self.session.refresh(result)
        return

    def login_user(self, user: UserLoginDTO) -> UserLoggedDTO:
        statement = select(User).where(
            User.email == user.email,
            User.hash == user.hash,
            User.deleted_at == None,
        )
        user_data = self.session.exec(statement).first()

        if not user_data:
            raise HandleException([GEN_2002], status.HTTP_401_UNAUTHORIZED)

        user_create = UserJWT.model_validate(user_data)

        token, token_expires = create_token(user_create.model_dump())

        user_response = UserLoggedDTO.model_validate(user_data)
        user_response.token = token
        user_response.expiration_date = token_expires
        user_response.picture_url = user_data.picture.url if user_data.picture else None
        user_response.user_name = f"{user_data.first_name} {user_data.last_name}"
        user_response.id = f"U-{user_response.user_id}"

        return user_response

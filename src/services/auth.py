import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import cast

import pytz
from fastapi import status
from sqlalchemy import func
from sqlalchemy.orm.session import Session

from core.classes.handle_exception import HandleException
from core.constants.generic_errors import GEN_2002, GEN_4000
from core.schemas.email import EmailMessage
from core.services.email import (
    MAIL_FROM,
    MAIL_PASSWORD,
    MAIL_PORT,
    MAIL_SERVER,
    MAIL_USERNAME,
    EmailService,
)
from core.utils.encrypt import create_token
from models.models import User, UserCode, UserRole
from schemas.auth import (
    UserCheckCodeDTO,
    UserForgotPasswordDTO,
    UserJWT,
    UserLoggedDTO,
    UserLoginDTO,
    UserResetPasswordDTO,
)


class AuthService:
    def __init__(self, db: Session, user: User | None):
        self.db = db
        self.current_user = user

    async def forgot_password(self, user: UserForgotPasswordDTO) -> None:
        result = (
            self.db.query(User)
            .filter(User.email == user.email, User.deleted_at == None)
            .first()
        )

        if not result:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        code = random.randint(100000, 999999)

        user_Code = UserCode(user_id=result.user_id, code=code)

        # Send Email
        subject = "Fake API - Change Password"
        fullName = f"{result.first_name} {result.last_name}"
        recipient = [user.email]
        message = EmailMessage(fullName=fullName, code=code).model_dump()

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

        self.db.add(user_Code)
        self.db.commit()
        self.db.refresh(user_Code)
        return

    def check_code(self, user: UserCheckCodeDTO) -> None:
        now = datetime.now(pytz.utc) - timedelta(hours=1)
        result: UserCode | None = (
            self.db.query(UserCode)
            .join(User, User.user_id == UserCode.user_id)
            .filter(
                UserCode.deleted_at == None,
                now < UserCode.created_at,
                UserCode.code == user.recovery_code,
                User.email == user.email,
            )
            .first()
        )

        if not result:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        result.deleted_at = cast(datetime, func.now())

        self.db.commit()
        self.db.refresh(result)
        return

    def reset_password(self, user: UserResetPasswordDTO) -> None:
        result: User | None = (
            self.db.query(User)
            .join(UserCode, User.user_id == UserCode.user_id)
            .filter(
                UserCode.code == user.recovery_code,
                User.email == user.email,
            )
            .first()
        )

        if not result:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        result.hash = user.hash if user.hash else ""

        self.db.commit()
        self.db.refresh(result)
        return

    def login_user(self, user: UserLoginDTO) -> UserLoggedDTO:
        result = (
            self.db.query(
                User,
                UserRole.role_id,
            )
            .join(
                UserRole,
                User.user_id == UserRole.user_id,
                isouter=True,
            )
            .filter(
                User.email == user.email,
                User.hash == user.hash,
                User.deleted_at == None,
                UserRole.deleted_at == None,
            )
            .first()
        )

        if not result:
            raise HandleException([GEN_2002], status.HTTP_401_UNAUTHORIZED)

        user_data, user_role_id = result

        user_create = UserJWT.model_validate(user_data)
        user_create.role_id = user_role_id

        token, token_expires = create_token(user_create.model_dump())

        user_response = UserLoggedDTO.model_validate(user_data)
        user_response.token = token
        user_response.expiration_date = token_expires
        user_response.role_id = user_role_id
        user_response.picture_url = user_data.picture.url if user_data.picture else None
        user_response.user_name = f"{user_data.first_name} {user_data.last_name}"
        user_response.id = f"U-{user_response.user_id}"

        return user_response

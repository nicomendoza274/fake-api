import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, cast

import pytz
from fastapi import status
from pydantic import TypeAdapter
from sqlalchemy import func
from sqlalchemy.orm.session import Session

from core.classes.generic_errors import GenericError
from core.constants.generic_errors import GEN_2002, GEN_4000
from core.schemas.email import EmailMessage
from core.schemas.success_schema import SuccessDTO
from core.services.base_service import BaseService
from core.services.email import (
    MAIL_FROM,
    MAIL_PASSWORD,
    MAIL_PORT,
    MAIL_SERVER,
    MAIL_USERNAME,
    EmailService,
)
from core.services.query import QueryCriterionService
from core.utils.encrypt import create_token, encrypt_string
from core.utils.query import str_to_query
from models.models import User, UserCode, UserRole
from schemas.user import (
    UserDTO,
    UserForgotChangePasswordDTO,
    UserJWT,
    UserLoggedDTO,
    UserLoginDTO,
    UserResponseDTO,
    UserSendCodeDTO,
    UserValidateCodeDTO,
)


class UserService(BaseService):
    def __init__(self, db: Session, user: User | None):
        self.db = db
        self.current_user = user
        self.sqlModel = User
        self.response_schema = UserResponseDTO

    def get_records(self, start: int | None, length: int | None, query: str | None):
        result = (
            self.db.query(
                User.user_id,
                User.email,
                User.first_name,
                User.last_name,
                UserRole.role_id,
            )
            .join(
                UserRole,
                User.user_id == UserRole.user_id,
                isouter=True,
            )
            .filter(
                User.deleted_at == None,
                UserRole.deleted_at == None,
            )
        )

        query_model = QueryCriterionService(self.sqlModel)

        query_criteria = str_to_query(query)

        result = query_model.sorts(query_criteria, result)
        result = query_model.filters(query_criteria, result)
        result = query_model.search(query_criteria, "name", result)
        result = result.order_by("user_id")

        if length:
            result = result.limit(length)

        if start:
            result = result.offset(start)

        result = result.all()
        total_count = len(result)

        user_list_adapter = TypeAdapter(List[UserResponseDTO])
        user_list_mapped = user_list_adapter.validate_python(result)

        response = self.get_multiple_response(
            count=total_count,
            start=start,
            length=len(result) if length == 0 else length,
            data=user_list_mapped,
        )

        return response

    def get_record(self, id: int):
        result = (
            self.db.query(
                User.user_id,
                User.email,
                User.first_name,
                User.last_name,
                UserRole.role_id,
            )
            .join(
                UserRole,
                User.user_id == UserRole.user_id,
                isouter=True,
            )
            .filter(
                User.deleted_at == None,
                UserRole.deleted_at == None,
                User.user_id == id,
            )
            .first()
        )

        if not result:
            raise GenericError(GEN_4000)

        data_response = UserResponseDTO.model_validate(result)
        response = self.get_response(data_response)

        return response

    def create_record(self, user: UserDTO):
        hash = encrypt_string(user.password)
        new_user = User(
            email=user.email,
            hash=hash,
            first_name=user.first_name,
            last_name=user.last_name,
        )

        if self.current_user:
            new_user.created_by = self.current_user.user_id

        self.db.add(new_user)
        self.db.flush()
        self.db.refresh(new_user)

        new_user_rol = UserRole(role_id=user.role_id, user_id=new_user.user_id)

        self.db.add(new_user_rol)
        self.db.flush()
        self.db.refresh(new_user_rol)

        userCreate = UserResponseDTO.model_validate(new_user)
        userCreate.role_id = user.role_id

        response = self.get_response(userCreate, status.HTTP_201_CREATED)
        self.db.commit()
        return response

    def update_record(self, user: UserDTO):

        hash = encrypt_string(user.password)
        user_data: User | None = (
            self.db.query(User)
            .filter(
                User.deleted_at == None,
                User.user_id == user.user_id,
            )
            .first()
        )

        if not user_data or not user.user_id:
            raise GenericError(GEN_4000)

        user_role_data: UserRole | None = (
            self.db.query(UserRole)
            .join(User, UserRole.user_id == User.user_id)
            .filter(
                UserRole.deleted_at == None,
                User.deleted_at == None,
                UserRole.user_id == user.user_id,
            )
            .first()
        )

        if not user_role_data:
            raise GenericError(GEN_4000)

        if self.current_user:
            user_data.updated_by = self.current_user.user_id

        user_data.updated_at = func.now()
        user_data.first_name = user.first_name
        user_data.last_name = user.last_name
        user_data.email = user.email
        user_data.hash = hash
        user_role_data.role_id = user.role_id

        user_updated = UserResponseDTO.model_validate(user)
        user_updated.role_id = user.role_id

        response = self.get_response(user_updated)
        self.db.commit()
        return response

    def delete_record(self, id: int):
        user_data = self.db.query(User).get(id)

        if not user_data or user_data.deleted_at != None:
            raise GenericError(GEN_4000)

        user_data.deleted_at = func.now()
        if self.current_user:
            user_data.deleted_by = self.current_user.user_id

        response = self.get_response(SuccessDTO())

        self.db.commit()
        return response

    async def send_code(self, user: UserSendCodeDTO):
        result = (
            self.db.query(User)
            .filter(User.email == user.email, User.deleted_at == None)
            .first()
        )

        if not result:
            raise GenericError(GEN_4000)

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
            content = SuccessDTO()
        except:
            print("Error to sent mail")
            content = {"success": True, "error": "Error to send mail"}

        self.db.add(user_Code)
        self.db.commit()
        self.db.refresh(user_Code)
        response = self.get_response(content)
        return response

    def validate_code(self, user: UserValidateCodeDTO):
        now = datetime.now(pytz.utc) - timedelta(hours=1)
        result: UserCode | None = (
            self.db.query(UserCode)
            .join(User, User.user_id == UserCode.user_id)
            .filter(
                UserCode.deleted_at == None,
                now < UserCode.created_at,
                UserCode.code == user.code,
                User.email == user.email,
            )
            .first()
        )

        if not result:
            raise GenericError(GEN_4000)

        result.deleted_at = cast(datetime, func.now())

        self.db.commit()
        self.db.refresh(result)
        content = SuccessDTO()
        response = self.get_response(content)

        return response

    def forgot_change_password(self, user: UserForgotChangePasswordDTO):
        result: User | None = (
            self.db.query(User)
            .join(UserCode, User.user_id == UserCode.user_id)
            .filter(
                UserCode.code == user.code,
                User.email == user.email,
            )
            .first()
        )

        if not result:
            raise GenericError(GEN_4000)

        result.hash = encrypt_string(user.newPassword)

        self.db.commit()
        self.db.refresh(result)
        content = SuccessDTO()
        response = self.get_response(content)

        return response

    def login_user(self, user: UserLoginDTO):
        hash = encrypt_string(user.password)
        result = (
            self.db.query(
                User.user_id,
                User.email,
                User.first_name,
                User.last_name,
                UserRole.role_id,
            )
            .join(
                UserRole,
                User.user_id == UserRole.user_id,
                isouter=True,
            )
            .filter(
                User.email == user.email,
                User.hash == hash,
                User.deleted_at == None,
                UserRole.deleted_at == None,
            )
            .first()
        )

        if not result:
            raise GenericError(GEN_2002)

        user_create = UserJWT.model_validate(result)

        token, token_expires = create_token(user_create.model_dump())

        user_response = UserLoggedDTO.model_validate(result)
        user_response.token = token
        user_response.expiration_date = token_expires

        response = self.get_response(user_response)

        return response

    def get_user_by_credentials(self, credentials: dict):
        result: User | None = (
            self.db.query(User)
            .filter(
                User.email == credentials["email"],
                User.deleted_at == None,
            )
            .first()
        )
        return result

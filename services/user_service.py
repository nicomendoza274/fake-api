import random
from datetime import datetime, timedelta
from typing import cast

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import DateTime, func
from sqlalchemy.orm.session import Session

from constants.error import GEN_2002, GEN_4000
from models.user import User as UserModel
from models.user_code import UserCode as UserCodeModel
from models.user_role import UserRole as UserRoleModel
from schemas.error import Errors
from schemas.user import (
    UserCreate,
    UserCreated,
    UserForgotChangePassword,
    UserList,
    UserLoged,
    UserLogin,
    UserSendCode,
    UserValidateCode,
)
from utils.email import send_email
from utils.encrypt import create_token, encrypt_string


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_credentials(self, credentials: dict):
        result: UserModel = (
            self.db.query(UserModel)
            .filter(UserModel.email == credentials["email"])
            .first()
        )
        return result

    def get_users(self):
        result = (
            self.db.query(
                UserModel.user_id,
                UserModel.email,
                UserModel.first_name,
                UserModel.last_name,
                UserRoleModel.role_id,
            )
            .join(
                UserRoleModel,
                UserModel.user_id == UserRoleModel.user_id,
                isouter=True,
            )
            .filter()
            .all()
        )

        users = [
            UserList(
                user_id=el[0],
                email=el[1],
                first_name=el[2],
                last_name=el[3],
                role_id=el[4],
            )
            for el in result
        ]

        return JSONResponse(status_code=200, content=jsonable_encoder(users))

    def create_user(self, user: UserCreate):
        new_user = UserModel(
            email=user.email,
            hash=encrypt_string(user.password),
            first_name=user.first_name,
            last_name=user.last_name,
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        new_user_rol = UserRoleModel(role_id=user.role_id, user_id=new_user.user_id)
        # new_user_rol.created_by = new_user.user_id

        self.db.add(new_user_rol)
        self.db.commit()
        self.db.refresh(new_user_rol)

        userCreate = UserCreated(
            user_id=new_user.user_id,
            email=new_user.email,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            role_id=user.role_id,
        )
        return JSONResponse(status_code=201, content=jsonable_encoder(userCreate))

    async def send_code(self, user: UserSendCode):
        result = self.db.query(UserModel).filter(UserModel.email == user.email).first()

        if not result:
            content = Errors(Errors=[GEN_4000]).model_dump()
            return JSONResponse(status_code=401, content=content)

        code = random.randint(100000, 999999)

        user_Code = UserCodeModel(user_id=result.user_id, code=code)

        # Send Email
        subject = "Fake API - Change Password"
        recipient = [user.email]
        message = {}
        message["fullName"] = f"{result.first_name} {result.last_name}"
        message["code"] = code

        try:
            await send_email(subject, recipient, message)
            content = {"data": {"success": True}}
        except:
            print("Error to sent mail")
            content = {"data": {"success": True, "error": "Error to send mail"}}
        finally:
            self.db.add(user_Code)
            self.db.commit()
            self.db.refresh(user_Code)
            return JSONResponse(status_code=200, content=content)

    def validate_code(self, user: UserValidateCode):
        tomorrow = datetime.now() + timedelta(hours=1)
        result: UserCodeModel = (
            self.db.query(UserCodeModel)
            .join(UserModel, UserModel.user_id == UserCodeModel.user_id)
            .filter(
                UserCodeModel.deleted_at == None,
                tomorrow < UserCodeModel.created_at,
                UserCodeModel.code == user.code,
                UserModel.email == user.email,
            )
            .first()
        )

        if not result:
            content = Errors(Errors=[GEN_4000]).model_dump()
            return JSONResponse(status_code=400, content=content)

        result.deleted_at = cast(datetime, func.now())

        self.db.commit()
        self.db.refresh(result)

        return JSONResponse(status_code=200, content={"data": {"success": True}})

    def forgot_change_password(self, user: UserForgotChangePassword):
        result: UserModel = (
            self.db.query(UserModel)
            .join(UserCodeModel, UserModel.user_id == UserCodeModel.user_id)
            .filter(
                UserCodeModel.code == user.code,
                UserModel.email == user.email,
            )
            .first()
        )

        if not result:
            content = Errors(Errors=[GEN_4000]).model_dump()
            return JSONResponse(status_code=401, content=content)

        result.hash = encrypt_string(user.newPassword)

        self.db.commit()
        self.db.refresh(result)

        return JSONResponse(status_code=200, content={"data": {"success": True}})

    def login_user(self, user: UserLogin):
        hash = encrypt_string(user.password)
        result = (
            self.db.query(UserModel, UserRoleModel)
            .join(
                UserRoleModel,
                UserModel.user_id == UserRoleModel.user_id,
                isouter=True,
            )
            .filter(UserModel.email == user.email, UserModel.hash == hash)
            .first()
        )

        if not result:
            content = Errors(Errors=[GEN_2002]).model_dump()
            return JSONResponse(status_code=401, content=content)

        user_data: UserModel = result[0]
        user_role_data: UserRoleModel = result[1]

        userCreate = UserCreated(
            user_id=user_data.user_id,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role_id=user_role_data.role_id,
        )

        token: str = create_token(userCreate.model_dump())

        user_response = UserLoged(
            user_id=userCreate.user_id,
            email=userCreate.email,
            first_name=userCreate.first_name,
            last_name=userCreate.last_name,
            token=token,
            role_id=userCreate.role_id,
        )

        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(user_response),
        )

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.session import Session

from models.user import User as UserModel
from schemas.user import UserCreate, UserLogin
from utils.encrypt import encrypt_string


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

    def create_user(self, user: UserLogin):
        new_user = UserModel(email=user.email, hash=encrypt_string(user.password))
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        userCreate = UserCreate.model_validate(jsonable_encoder(new_user))
        return userCreate

    def login_user(self, user: UserLogin):
        hash = encrypt_string(user.password)
        result: UserModel = (
            self.db.query(UserModel)
            .filter(UserModel.email == user.email, UserModel.hash == hash)
            .first()
        )

        if not result:
            return None

        userCreate = UserCreate.model_validate(jsonable_encoder(result))

        return userCreate

    def get_users(self):
        result = self.db.query(UserModel).filter().all()
        users = [UserCreate.model_validate(jsonable_encoder(el)) for el in result]
        return users

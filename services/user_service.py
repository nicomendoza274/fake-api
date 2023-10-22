from sqlalchemy.orm.session import Session

from models.user import User as UserModel
from schemas.user import User
from services.encrypt import encrypt_string


class UserService:
    def __init__(self, db: Session) -> UserModel | None:
        self.db = db

    def get_user_by_credentials(self, credentials: dict):
        result: UserModel = (
            self.db.query(UserModel)
            .filter(
                UserModel.email == credentials["email"],
                UserModel.hash == credentials["hash"],
            )
            .first()
        )
        return result

    def login_user(self, user: User) -> UserModel | None:
        hash = encrypt_string(user.password)
        result: UserModel = (
            self.db.query(UserModel)
            .filter(UserModel.email == user.email, UserModel.hash == hash)
            .first()
        )
        return result

    def create_user(self, user: User) -> User:
        new_user = UserModel(email=user.email, hash=encrypt_string(user.password))
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

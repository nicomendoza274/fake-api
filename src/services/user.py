from dataclasses import dataclass
from datetime import datetime, timezone

from fastapi import status
from sqlmodel import select

from core.classes.handle_exception import HandleException
from core.constants.generic_errors import GEN_2001, GEN_4000
from core.database.database import SessionDep
from core.services.base import BaseService
from models.user import User, UserChangePasswordDTO, UserDTO, UserResponseDTO


@dataclass
class UserService(BaseService[User, UserResponseDTO, UserDTO]):
    session: SessionDep
    current_user: User | None
    sql_model: type[User] = User
    response_schema: type[UserResponseDTO] = UserResponseDTO

    def change_password(self, user: UserChangePasswordDTO):

        if not self.current_user:
            raise HandleException([GEN_2001], status.HTTP_401_UNAUTHORIZED)

        statement = select(User).where(
            User.deleted_at == None,
            User.user_id == self.current_user.user_id,
        )
        user_data = self.session.exec(statement).first()

        if not user_data:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        user_data.hash = str(user.hash)
        user_data.updated_at = datetime.now(timezone.utc)
        user_data.updated_by = self.current_user.user_id

        self.session.flush()
        self.session.refresh(user_data)

        self.session.commit()
        return

    def get_user_by_credentials(self, credentials: dict):
        statement = select(User).where(
            User.user_id == credentials["user_id"],
            User.deleted_at == None,
        )
        result = self.session.exec(statement).first()
        return result

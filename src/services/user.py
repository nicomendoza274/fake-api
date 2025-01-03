from datetime import datetime, timezone

from fastapi import status
from sqlmodel import select

from core.classes.handle_exception import HandleException
from core.constants.generic_errors import GEN_2001, GEN_4000
from core.database.database import SessionDep
from core.services.base import BaseService
from models.user import User, UserChangePasswordDTO, UserDTO, UserResponseDTO
from models.user_role import UserRole


class UserService(BaseService[User, UserResponseDTO, UserDTO]):
    def __init__(self, session: SessionDep, user: User | None):
        super().__init__(session, user, User, UserResponseDTO)

    def create_record(self, user: UserDTO) -> None:

        new_user = User(**user.model_dump())

        if self.current_user:
            new_user.created_by = self.current_user.user_id

        self.session.add(new_user)
        self.session.flush()
        self.session.refresh(new_user)

        new_user_rol = UserRole(
            user_role_id=None,
            role_id=user.role_id,
            user_id=new_user.user_id,
        )

        self.session.add(new_user_rol)
        self.session.flush()
        self.session.refresh(new_user_rol)

        userCreate = UserResponseDTO.model_validate(new_user)
        userCreate.role_id = user.role_id

        self.session.commit()
        return

    def update_record(self, user: UserDTO, id: int) -> None:

        if not self.current_user:
            raise HandleException([GEN_2001], status.HTTP_401_UNAUTHORIZED)

        statement = (
            select(User, UserRole.role_id)
            .join(UserRole, UserRole.user_id == User.user_id, isouter=True)  # type: ignore
            .where(
                User.deleted_at == None,
                UserRole.deleted_at == None,
                User.user_id == id,
            )
        )
        result = self.session.exec(statement).first()

        if not result:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        user_data, _ = result

        updated_by = self.current_user.user_id if self.current_user else None

        user_data.updated_at = datetime.now(timezone.utc)
        user_data.updated_by = updated_by
        user_data.first_name = user.first_name
        user_data.last_name = user.last_name
        user_data.email = user.email
        user_data.picture_id = user.picture_id
        user_data.hash = str(user.hash) if user.hash else ""

        self.session.commit()
        return

    def delete_record(self, id: int) -> None:
        user_data = self.session.get(User, id)

        if not user_data or user_data.deleted_at != None:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        user_data.deleted_at = datetime.now(timezone.utc)
        if self.current_user:
            user_data.deleted_by = self.current_user.user_id

        self.session.commit()
        return

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

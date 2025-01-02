from datetime import datetime, timezone

from fastapi import status
from sqlmodel import select

from core.classes.handle_exception import HandleException
from core.constants.generic_errors import GEN_2001, GEN_4000
from core.database.database import SessionDep
from core.models.query import QueryCriteria
from core.services.base import BaseService
from core.services.query import QueryCriterionService
from models.user import User, UserChangePasswordDTO, UserDTO, UserResponseDTO
from models.user_role import UserRole


class UserService(BaseService[User, UserResponseDTO, UserDTO]):
    def __init__(self, session: SessionDep, user: User | None):
        super().__init__(session, user, User, UserResponseDTO)

    def get_records(
        self,
        start: int | None,
        length: int | None,
        query_criteria: QueryCriteria | None,
    ) -> tuple[list[UserResponseDTO], int]:

        statement = (
            select(User, UserRole.role_id)
            .join(UserRole, UserRole.user_id == User.user_id, isouter=True)  # type: ignore
            .where(
                User.deleted_at == None,
                UserRole.deleted_at == None,
            )
        )

        query_model = QueryCriterionService(self.sqlModel, query_criteria)

        statement = self.filter_list(query_model, statement)
        statement = self.search_list(query_model, statement)
        statement = self.sort_list(query_model, statement)
        statement = self.sort_by_pk(statement)

        total_count = len(self.session.exec(statement).all())

        if length:
            statement = statement.limit(length)

        if start:
            statement = statement.offset(start)

        results = self.session.exec(statement).all()

        mapped_users: list[UserResponseDTO] = []
        for result in results:
            user_data, user_role_id = result
            mapped_user = UserResponseDTO.model_validate(user_data)
            mapped_user.role_id = user_role_id
            mapped_users.append(mapped_user)

        return mapped_users, total_count

    def get_record(self, id: int) -> UserResponseDTO:
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

        user_data, user_role_id = result

        data_response = UserResponseDTO.model_validate(user_data)
        data_response.role_id = user_role_id

        return data_response

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

        statement = (
            select(User, UserRole.role_id)
            .join(UserRole, UserRole.user_id == User.user_id, isouter=True)  # type: ignore
            .where(
                User.deleted_at == None,
                UserRole.deleted_at == None,
                User.user_id == self.current_user.user_id,
            )
        )
        result = self.session.exec(statement).first()

        if not result:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        user_data, role_id = result

        user_data.hash = str(user.hash)
        user_data.updated_at = datetime.now(timezone.utc)

        if self.current_user:
            user_data.updated_by = self.current_user.user_id

        self.session.flush()
        self.session.refresh(user_data)

        user_update_password = UserResponseDTO.model_validate(user_data)
        user_update_password.role_id = role_id

        self.session.commit()
        return

    def get_user_by_credentials(self, credentials: dict):
        statement = select(User).where(
            User.user_id == credentials["user_id"],
            User.deleted_at == None,
        )
        result = self.session.exec(statement).first()
        return result

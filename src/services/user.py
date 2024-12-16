from fastapi import status
from sqlalchemy import func

from core.classes.handle_exception import HandleException
from core.constants.generic_errors import GEN_2001, GEN_4000
from core.database.database import SessionDep
from core.schemas.query import QueryCriteria
from core.services.base_service import BaseService
from core.services.query import QueryCriterionService
from models.models import User, UserRole
from schemas.user import UserChangePasswordDTO, UserDTO, UserResponseDTO


class UserService(BaseService[User, UserResponseDTO, UserDTO]):
    def __init__(self, session: SessionDep, user: User | None):
        super().__init__(session, user, User, UserResponseDTO)

    def get_records(
        self,
        start: int | None,
        length: int | None,
        query_criteria: QueryCriteria | None,
    ) -> tuple[list[UserResponseDTO], int]:
        results = (
            self.session.query(
                User,
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

        query_model = QueryCriterionService(self.sqlModel, query_criteria)

        results = self.filter_list(query_model, results)
        results = self.search_list(query_model, results)
        results = self.sort_list(query_model, results)
        results = self.sort_by_pk(results)

        total_count = len(results.all())

        if length:
            results = results.limit(length)

        if start:
            results = results.offset(start)

        results = results.all()

        mapped_users: list[UserResponseDTO] = []
        for result in results:
            user_data, user_role_id = result
            mapped_user = UserResponseDTO.model_validate(user_data)
            mapped_user.role_id = user_role_id
            mapped_users.append(mapped_user)

        return mapped_users, total_count

    def get_record(self, id: int) -> UserResponseDTO:
        result = (
            self.session.query(
                User,
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
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        user_data, user_role_id = result

        data_response = UserResponseDTO.model_validate(user_data)
        data_response.role_id = user_role_id

        return data_response

    def create_record(self, user: UserDTO) -> None:

        dto_dict = user.model_dump()
        user_dict = {
            key: value
            for key, value in dto_dict.items()
            if key in User.__table__.columns
        }
        new_user = User(**user_dict)

        if self.current_user:
            new_user.created_by = self.current_user.user_id

        self.session.add(new_user)
        self.session.flush()
        self.session.refresh(new_user)

        new_user_rol = UserRole(role_id=user.role_id, user_id=new_user.user_id)

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

        result = (
            self.session.query(
                User,
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
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        user_data, _ = result

        updated_by = self.current_user.user_id if self.current_user else None

        user_data.updated_at = func.now()
        user_data.updated_by = updated_by
        user_data.first_name = user.first_name
        user_data.last_name = user.last_name
        user_data.email = user.email
        user_data.role_id = user.role_id
        user_data.picture_id = user.picture_id
        user_data.hash = user.hash

        self.session.commit()
        return

    def delete_record(self, id: int) -> None:
        user_data = self.session.query(User).get(id)

        if not user_data or user_data.deleted_at != None:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        user_data.deleted_at = func.now()
        if self.current_user:
            user_data.deleted_by = self.current_user.user_id

        self.session.commit()
        return

    def change_password(self, user: UserChangePasswordDTO):

        if not self.current_user:
            raise HandleException([GEN_2001], status.HTTP_401_UNAUTHORIZED)

        result = (
            self.session.query(
                User,
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
                User.user_id == self.current_user.user_id,
            )
            .first()
        )

        if not result:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        user_data, role_id = result

        user_data.hash = user.hash
        user_data.updated_at = func.now()

        if self.current_user:
            user_data.updated_by = self.current_user.user_id

        self.session.flush()
        self.session.refresh(user_data)

        user_update_password = UserResponseDTO.model_validate(user_data)
        user_update_password.role_id = role_id

        self.session.commit()
        return

    def get_user_by_credentials(self, credentials: dict):
        result: User | None = (
            self.session.query(User)
            .filter(
                User.user_id == credentials["user_id"],
                User.deleted_at == None,
            )
            .first()
        )
        return result

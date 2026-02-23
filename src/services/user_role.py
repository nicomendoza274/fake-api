from src.core.database.database import SessionDep
from src.core.services.base import BaseService
from src.models.user import User
from src.models.user_role import UserRole, UserRoleDTO, UserRoleResponseDTO


class UserRoleService(BaseService[UserRole, UserRoleResponseDTO, UserRoleDTO]):
    session: SessionDep
    current_user: User
    sql_model: type[UserRole] = UserRole
    response_schema: type[UserRoleResponseDTO] = UserRoleResponseDTO

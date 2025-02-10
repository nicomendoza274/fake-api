from core.database.database import SessionDep
from core.services.base import BaseService
from models.user import User
from models.user_role import UserRole, UserRoleDTO, UserRoleResponseDTO


class UserRoleService(BaseService[UserRole, UserRoleResponseDTO, UserRoleDTO]):
    session: SessionDep
    current_user: User
    sql_model: type[UserRole] = UserRole
    response_schema: type[UserRoleResponseDTO] = UserRoleResponseDTO

from core.database.database import SessionDep
from core.services.base import BaseService
from models.user import User
from models.user_role import UserRole, UserRoleDTO, UserRoleResponseDTO


class UserRoleService(BaseService[UserRole, UserRoleResponseDTO, UserRoleDTO]):
    def __init__(self, session: SessionDep, user: User) -> None:
        super().__init__(session, user, UserRole, UserRoleResponseDTO)

from core.database.database import SessionDep
from core.services.base_service import BaseService
from models.models import User, UserRole
from schemas.user_role import UserRoleDTO, UserRoleResponseDTO


class UserRoleService(BaseService[UserRole, UserRoleResponseDTO, UserRoleDTO]):
    def __init__(self, session: SessionDep, user: User) -> None:
        super().__init__(session, user, UserRole, UserRoleResponseDTO)

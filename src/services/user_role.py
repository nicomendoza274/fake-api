from sqlalchemy.orm.session import Session

from core.services.base_service import BaseService
from models.models import User, UserRole
from schemas.user_role import UserRoleDTO, UserRoleResponseDTO


class UserRoleService(BaseService[UserRole, UserRoleResponseDTO, UserRoleDTO]):
    def __init__(self, db: Session, user: User) -> None:
        super().__init__(db, user, UserRole, UserRoleResponseDTO)

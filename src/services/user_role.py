from sqlalchemy.orm.session import Session

from core.services.base_service import BaseService
from models.models import User, UserRole
from schemas.user_role import UserRoleResponseDTO


class UserRoleService(BaseService):
    def __init__(self, db: Session, user: User) -> None:
        super().__init__(db, user, UserRole, UserRoleResponseDTO)

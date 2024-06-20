from sqlalchemy.orm.session import Session

from core.services.base_service import BaseService
from models.models import Role, User
from schemas.role import RoleResponseDTO


class RoleService(BaseService):
    def __init__(self, db: Session, user: User) -> None:
        super().__init__(db, user, Role, RoleResponseDTO)

from sqlalchemy.orm.session import Session

from core.services.base_service import BaseService
from models.models import Role, User
from schemas.role import RoleDTO, RoleResponseDTO


class RoleService(BaseService[Role, RoleResponseDTO, RoleDTO]):
    def __init__(self, db: Session, user: User) -> None:
        super().__init__(db, user, Role, RoleResponseDTO)

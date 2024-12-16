from core.database.database import SessionDep
from core.services.base_service import BaseService
from models.models import Role, User
from schemas.role import RoleDTO, RoleResponseDTO


class RoleService(BaseService[Role, RoleResponseDTO, RoleDTO]):
    def __init__(self, session: SessionDep, user: User) -> None:
        super().__init__(session, user, Role, RoleResponseDTO)

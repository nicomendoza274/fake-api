from core.database.database import SessionDep
from core.services.base import BaseService
from models.role import Role, RoleDTO, RoleResponseDTO
from models.user import User


class RoleService(BaseService[Role, RoleResponseDTO, RoleDTO]):
    def __init__(self, session: SessionDep, user: User) -> None:
        super().__init__(session, user, Role, RoleResponseDTO)

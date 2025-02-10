from dataclasses import dataclass

from core.database.database import SessionDep
from core.services.base import BaseService
from models.role import Role, RoleDTO, RoleResponseDTO
from models.user import User


@dataclass
class RoleService(BaseService[Role, RoleResponseDTO, RoleDTO]):
    session: SessionDep
    current_user: User
    sql_model: type[Role] = Role
    response_schema: type[RoleResponseDTO] = RoleResponseDTO

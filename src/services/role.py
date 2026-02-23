from dataclasses import dataclass

from src.core.database.database import SessionDep
from src.core.services.base import BaseService
from src.models.role import Role, RoleDTO, RoleResponseDTO
from src.models.user import User


@dataclass
class RoleService(BaseService[Role, RoleResponseDTO, RoleDTO]):
    session: SessionDep
    current_user: User
    sql_model: type[Role] = Role
    response_schema: type[RoleResponseDTO] = RoleResponseDTO

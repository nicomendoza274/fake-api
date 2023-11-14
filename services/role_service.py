from sqlalchemy.orm.session import Session

from models.role import Role as RoleModel
from schemas.role import Role
from services.base_service import BaseService


class RoleService(BaseService):
    def __init__(self, db: Session) -> None:
        self.db = db
        self.sqlModel = RoleModel
        self.model = Role

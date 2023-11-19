from sqlalchemy.orm.session import Session

from models.role import Role as RoleModel
from models.user import User as UserModel
from schemas.role import Role
from services.base_service import BaseService


class RoleService(BaseService):
    def __init__(self, db: Session, user: UserModel) -> None:
        self.db = db
        self.current_user = user
        self.sqlModel = RoleModel
        self.model = Role

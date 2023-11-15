from sqlalchemy.orm.session import Session

from models.user_role import UserRole as UserRoleModel
from schemas.user_role import UserRole
from services.base_service import BaseService


class UserRoleService(BaseService):
    def __init__(self, db: Session) -> None:
        self.db = db
        self.sqlModel = UserRoleModel
        self.model = UserRole

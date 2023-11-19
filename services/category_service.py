from sqlalchemy.orm.session import Session

from models.category import Category as CategoryModel
from models.user import User as UserModel
from schemas.category import Category
from services.base_service import BaseService


class CategoryService(BaseService):
    def __init__(self, db: Session, user: UserModel) -> None:
        self.db = db
        self.current_user = user
        self.sqlModel = CategoryModel
        self.model = Category

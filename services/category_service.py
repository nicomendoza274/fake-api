from sqlalchemy.orm.session import Session

from models.category import Category as CategoryModel
from schemas.category import Category
from services.base_service import BaseService


class CategoryService(BaseService):
    def __init__(self, db: Session) -> None:
        self.db = db
        self.sqlModel = CategoryModel
        self.model = Category

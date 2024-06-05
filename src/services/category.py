from sqlalchemy.orm.session import Session

from core.services.base_service import BaseService
from models.models import Category, User
from schemas.category import CategoryResponseDTO


class CategoryService(BaseService):
    def __init__(self, db: Session, user: User) -> None:
        self.db = db
        self.current_user = user
        self.sqlModel = Category
        self.response_schema = CategoryResponseDTO

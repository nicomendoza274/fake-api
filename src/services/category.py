from sqlalchemy.orm.session import Session

from core.services.base_service import BaseService
from models.models import Category, User
from schemas.category import CategoryDTO, CategoryResponseDTO


class CategoryService(BaseService[Category, CategoryResponseDTO, CategoryDTO]):
    def __init__(self, db: Session, user: User) -> None:
        super().__init__(
            db=db,
            current_user=user,
            sqlModel=Category,
            response_schema=CategoryResponseDTO,
        )

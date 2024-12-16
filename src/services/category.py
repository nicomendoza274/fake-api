from core.database.database import SessionDep
from core.services.base_service import BaseService
from models.models import Category, User
from schemas.category import CategoryDTO, CategoryResponseDTO


class CategoryService(BaseService[Category, CategoryResponseDTO, CategoryDTO]):
    def __init__(self, session: SessionDep, user: User) -> None:
        super().__init__(
            session=session,
            current_user=user,
            sqlModel=Category,
            response_schema=CategoryResponseDTO,
        )

from core.database.database import SessionDep
from core.services.base import BaseService
from models.category import Category, CategoryDTO, CategoryResponseDTO
from models.user import User


class CategoryService(BaseService[Category, CategoryResponseDTO, CategoryDTO]):
    def __init__(self, session: SessionDep, user: User) -> None:
        super().__init__(
            session=session,
            current_user=user,
            sqlModel=Category,
            response_schema=CategoryResponseDTO,
        )

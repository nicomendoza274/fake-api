from dataclasses import dataclass

from src.core.database.database import SessionDep
from src.core.services.base import BaseService
from src.models.category import Category, CategoryDTO, CategoryResponseDTO
from src.models.user import User


@dataclass
class CategoryService(BaseService[Category, CategoryResponseDTO, CategoryDTO]):
    session: SessionDep
    current_user: User
    sql_model: type[Category] = Category
    response_schema: type[CategoryResponseDTO] = CategoryResponseDTO

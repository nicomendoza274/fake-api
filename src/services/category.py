from dataclasses import dataclass

from core.database.database import SessionDep
from core.services.base import BaseService
from models.category import Category, CategoryDTO, CategoryResponseDTO
from models.user import User


@dataclass
class CategoryService(BaseService[Category, CategoryResponseDTO, CategoryDTO]):
    session: SessionDep
    current_user: User
    sql_model: type[Category] = Category
    response_schema: type[CategoryResponseDTO] = CategoryResponseDTO

from dataclasses import dataclass

from sqlmodel import select

from src.core.database.database import SessionDep
from src.core.models.file import File
from src.core.models.query import PropertyModel
from src.core.services.base import BaseService
from src.models.category import Category
from src.models.product import Product, ProductDTO, ProductResponseDTO
from src.models.user import User


@dataclass
class ProductService(BaseService[Product, ProductResponseDTO, ProductDTO]):
    session: SessionDep
    current_user: User
    sql_model: type[Product] = Product
    response_schema: type[ProductResponseDTO] = ProductResponseDTO

    def get_result(self):
        return self.session.exec(
            select(Product)
            .join(Category, Product.category, isouter=True)  # type: ignore
            .where(Product.deleted_at == None)
        )

    def get_optimized_statement(self, base_statement):
        """Get optimized statement with joins to avoid N+1 queries"""
        return base_statement.join(
            Category, Product.category, isouter=True  # type: ignore
        ).join(
            File, Product.picture, isouter=True  # type: ignore
        )

    def get_property_model_list(self) -> list[PropertyModel]:
        return [
            PropertyModel(property="category", model=Category),
        ]

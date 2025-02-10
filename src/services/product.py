from dataclasses import dataclass

from sqlmodel import select

from core.database.database import SessionDep
from core.models.query import PropertyModel
from core.services.base import BaseService
from models.category import Category
from models.product import Product, ProductDTO, ProductResponseDTO
from models.user import User


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

    def get_property_model_list(self) -> list[PropertyModel]:
        return [
            PropertyModel(property="category", model=Category),
        ]

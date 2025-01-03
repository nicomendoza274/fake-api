from sqlmodel import select

from core.database.database import SessionDep
from core.models.query import PropertyModel
from core.services.base import BaseService
from models.category import Category
from models.product import Product, ProductDTO, ProductResponseDTO
from models.user import User


class ProductService(BaseService[Product, ProductResponseDTO, ProductDTO]):
    def __init__(self, session: SessionDep, user: User) -> None:
        super().__init__(session, user, Product, ProductResponseDTO)

        statement = (
            select(Product)
            .join(Category, Product.category, isouter=True)  # type: ignore
            .where(Product.deleted_at == None)
        )
        self.result = self.session.exec(statement)

        self.property_model_list = [
            PropertyModel(property="category", model=Category),
        ]

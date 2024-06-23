from sqlalchemy.orm.session import Session

from core.schemas.query import PropertyModel
from core.services.base_service import BaseService
from models.models import Category, Product, User
from schemas.product import ProductResponseDTO


class ProductService(BaseService):
    def __init__(self, db: Session, user: User) -> None:
        super().__init__(db, user, Product, ProductResponseDTO)

        self.result = (
            self.db.query(Product)
            .join(Category, Product.category, isouter=True)
            .filter(Product.deleted_at == None)
        )

        self.property_model_list = [
            PropertyModel(property="category", model=Category),
        ]

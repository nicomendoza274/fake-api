from core.database.database import SessionDep
from core.schemas.query import PropertyModel
from core.services.base_service import BaseService
from models.models import Category, Product, User
from schemas.product import ProductDTO, ProductResponseDTO


class ProductService(BaseService[Product, ProductResponseDTO, ProductDTO]):
    def __init__(self, session: SessionDep, user: User) -> None:
        super().__init__(session, user, Product, ProductResponseDTO)

        self.result = (
            self.session.query(Product)
            .join(Category, Product.category, isouter=True)
            .filter(Product.deleted_at == None)
        )

        self.property_model_list = [
            PropertyModel(property="category", model=Category),
        ]

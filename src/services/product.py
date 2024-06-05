from sqlalchemy.orm.session import Session

from core.services.base_service import BaseService
from models.models import Product, User
from schemas.product import ProductResponseDTO


class ProductService(BaseService):
    def __init__(self, db: Session, user: User) -> None:
        self.db = db
        self.current_user = user
        self.sqlModel = Product
        self.response_schema = ProductResponseDTO

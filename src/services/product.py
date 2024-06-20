from sqlalchemy.orm.session import Session

from core.services.base_service import BaseService
from models.models import Product, User
from schemas.product import ProductResponseDTO


class ProductService(BaseService):
    def __init__(self, db: Session, user: User) -> None:
        super().__init__(db, user, Product, ProductResponseDTO)

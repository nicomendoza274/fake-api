from sqlalchemy.orm.session import Session

from models.product import Product as ProductModel
from schemas.product import Product
from services.base_service import BaseService


class ProductService(BaseService):
    def __init__(self, db: Session) -> None:
        self.db = db
        self.sqlModel = ProductModel
        self.model = Product

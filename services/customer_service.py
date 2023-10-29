from sqlalchemy.orm.session import Session

from models.customer import Customer as CustomerModel
from schemas.customer import Customer
from services.base_service import BaseService


class CustomerService(BaseService):
    def __init__(self, db: Session):
        self.db = db
        self.schema = CustomerModel
        self.model = Customer

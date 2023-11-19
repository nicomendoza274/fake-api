from sqlalchemy.orm.session import Session

from models.customer import Customer as CustomerModel
from models.user import User as UserModel
from schemas.customer import Customer
from services.base_service import BaseService


class CustomerService(BaseService):
    def __init__(self, db: Session, user: UserModel):
        self.db = db
        self.current_user = user
        self.sqlModel = CustomerModel
        self.model = Customer

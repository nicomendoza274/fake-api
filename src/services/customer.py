from sqlalchemy.orm.session import Session

from core.services.base_service import BaseService
from models.models import Customer, User
from schemas.customer import CustomerDTO, CustomerResponseDTO


class CustomerService(BaseService[Customer, CustomerResponseDTO, CustomerDTO]):
    def __init__(self, db: Session, user: User):
        super().__init__(db, user, Customer, CustomerResponseDTO)

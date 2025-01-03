from core.database.database import SessionDep
from core.services.base import BaseService
from models.customer import Customer, CustomerDTO, CustomerResponseDTO
from models.user import User


class CustomerService(BaseService[Customer, CustomerResponseDTO, CustomerDTO]):
    def __init__(self, session: SessionDep, user: User):
        super().__init__(session, user, Customer, CustomerResponseDTO)

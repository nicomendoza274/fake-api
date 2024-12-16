from core.database.database import SessionDep
from core.services.base_service import BaseService
from models.models import Customer, User
from schemas.customer import CustomerDTO, CustomerResponseDTO


class CustomerService(BaseService[Customer, CustomerResponseDTO, CustomerDTO]):
    def __init__(self, session: SessionDep, user: User):
        super().__init__(session, user, Customer, CustomerResponseDTO)

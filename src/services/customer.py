from dataclasses import dataclass

from core.database.database import SessionDep
from core.services.base import BaseService
from models.customer import Customer, CustomerDTO, CustomerResponseDTO
from models.user import User


@dataclass
class CustomerService(BaseService[Customer, CustomerResponseDTO, CustomerDTO]):
    session: SessionDep
    current_user: User
    sql_model: type[Customer] = Customer
    response_schema: type[CustomerResponseDTO] = CustomerResponseDTO

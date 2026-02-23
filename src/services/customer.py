from dataclasses import dataclass

from src.core.database.database import SessionDep
from src.core.services.base import BaseService
from src.models.customer import Customer, CustomerDTO, CustomerResponseDTO
from src.models.user import User


@dataclass
class CustomerService(BaseService[Customer, CustomerResponseDTO, CustomerDTO]):
    session: SessionDep
    current_user: User
    sql_model: type[Customer] = Customer
    response_schema: type[CustomerResponseDTO] = CustomerResponseDTO

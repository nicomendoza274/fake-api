from fastapi import APIRouter, Depends, Path, status

from core.database.database import SessionDep
from core.models.response import MultipleResponseData, ResponseData
from core.utils.query import str_to_query
from core.utils.response import get_empty_response, get_multiple_response, get_response
from middlewares.jwt_bearer import JWTBearer
from models.customer import CustomerDTO, CustomerResponseDTO
from models.user import User
from services.customer import CustomerService

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.get(
    "",
    response_model=MultipleResponseData[list[CustomerResponseDTO]],
)
def list_data(
    session: SessionDep,
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    user: User = Depends(JWTBearer()),
):
    query_criteria = str_to_query(query)
    customer_list, total_count = CustomerService(session, user).get_records(
        start, length, query_criteria
    )
    response = get_multiple_response(
        count=total_count,
        start=start,
        length=len(customer_list) if length == 0 else length,
        data=customer_list,
    )
    return response


@router.get(
    "/{customerId}",
    response_model=ResponseData[CustomerResponseDTO],
)
def get_data(
    session: SessionDep,
    customer_id: int = Path(alias="customerId"),
    user: User = Depends(JWTBearer()),
):
    customer_data = CustomerService(session, user).get_record(customer_id)
    response = get_response(customer_data)
    return response


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
def create_data(
    customer: CustomerDTO,
    session: SessionDep,
    user: User = Depends(JWTBearer()),
):
    CustomerService(session, user).create_record(customer)
    response = get_empty_response(status.HTTP_201_CREATED)
    return response


@router.put(
    "/{customerId}",
    response_model=None,
)
def update_data(
    customer: CustomerDTO,
    session: SessionDep,
    customer_id: int = Path(alias="customerId"),
    user: User = Depends(JWTBearer()),
):
    CustomerService(session, user).update_record(customer, customer_id)
    response = get_empty_response()
    return response


@router.delete(
    "/{customerId}",
    response_model=None,
)
def delete_data(
    session: SessionDep,
    customer_id: int = Path(alias="customerId"),
    user: User = Depends(JWTBearer()),
):
    CustomerService(session, user).delete_record(customer_id)
    response = get_empty_response()
    return response

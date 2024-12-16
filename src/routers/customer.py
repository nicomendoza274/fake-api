from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm.session import Session

from core.database.database import get_db
from core.schemas.response import MultipleResponseData, ResponseData
from core.utils.query import str_to_query
from core.utils.response import get_empty_response, get_multiple_response, get_response
from middlewares.jwt_bearer import JWTBearer
from models.models import User
from schemas.customer import CustomerDTO, CustomerResponseDTO
from services.customer import CustomerService

customer = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@customer.get(
    "",
    response_model=MultipleResponseData[list[CustomerResponseDTO]],
)
def list_data(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    query_criteria = str_to_query(query)
    customer_list, total_count = CustomerService(db, user).get_records(
        start, length, query_criteria
    )
    response = get_multiple_response(
        count=total_count,
        start=start,
        length=len(customer_list) if length == 0 else length,
        data=customer_list,
    )
    return response


@customer.get(
    "/{customerId}",
    response_model=ResponseData[CustomerResponseDTO],
)
def get(
    customer_id: int = Path(alias="customerId"),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    customer_data = CustomerService(db, user).get_record(customer_id)
    response = get_response(customer_data)
    return response


@customer.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
def create(
    customer: CustomerDTO,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    CustomerService(db, user).create_record(customer)
    response = get_empty_response(status.HTTP_201_CREATED)
    return response


@customer.put(
    "/{customerId}",
    response_model=None,
)
def update(
    customer: CustomerDTO,
    customer_id: int = Path(alias="customerId"),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    CustomerService(db, user).update_record(customer, customer_id)
    response = get_empty_response()
    return response


@customer.delete(
    "/multiple",
    response_model=None,
)
async def delete_multiple(
    ids: list[int] = Query(...),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    CustomerService(db, user).delete_multiple(ids)
    response = get_empty_response()
    return response


@customer.delete(
    "/{customerId}",
    response_model=None,
)
def delete(
    customer_id: int = Path(alias="customerId"),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    CustomerService(db, user).delete_record(customer_id)
    response = get_empty_response()
    return response

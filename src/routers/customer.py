from fastapi import APIRouter, Depends, Path, Query, status

from src.core.constants.responses import NOT_200, NOT_201, NOT_422
from src.core.database.database import SessionDep
from src.core.models.response import MultipleResponseData, ResponseData
from src.core.utils.query import str_to_query
from src.core.utils.response import (
    get_empty_response,
    get_multiple_response,
    get_response,
)
from src.middlewares.jwt_bearer import JWTBearer
from src.models.customer import CustomerDTO, CustomerResponseDTO
from src.models.user import User
from src.services.customer import CustomerService

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.get(
    path="",
    response_model=MultipleResponseData[CustomerResponseDTO],
    responses=NOT_422,
    summary="List customers",
)
def list_data(
    session: SessionDep,
    start: int | None = Query(default=0, description="Starting index for pagination"),
    length: int | None = Query(default=15, description="Number of items per page"),
    query: str | None = Query(default=None, description="Base64 encoded string"),
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
    path="/{customerId}",
    response_model=ResponseData[CustomerResponseDTO],
    responses=NOT_422,
    summary="Get customer",
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
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
    responses=NOT_422 | NOT_201,
    summary="Create customer",
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
    path="/{customerId}",
    response_model=None,
    responses=NOT_422 | NOT_200,
    summary="Update customer",
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
    path="/{customerId}",
    response_model=None,
    responses=NOT_422 | NOT_200,
    summary="Delete customer",
)
def delete_data(
    session: SessionDep,
    customer_id: int = Path(alias="customerId"),
    user: User = Depends(JWTBearer()),
):
    CustomerService(session, user).delete_record(customer_id)
    response = get_empty_response()
    return response

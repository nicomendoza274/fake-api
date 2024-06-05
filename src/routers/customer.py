from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm.session import Session

from core.database.database import get_db
from core.schemas.response import MultipleResponseData, ResponseData
from core.schemas.success_schema import SuccessDTO
from middlewares.jwt_bearer import JWTBearer
from models.models import User
from schemas.customer import CustomerDTO, CustomerResponseDTO
from services.customer import CustomerService

customer_router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@customer_router.get(
    "",
    response_model=MultipleResponseData[List[CustomerResponseDTO]],
)
def list(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = CustomerService(db, user).get_records(start, length, query)
    return response


@customer_router.get(
    "/{id}",
    response_model=ResponseData[CustomerResponseDTO],
)
def get(id: int, db: Session = Depends(get_db), user: User = Depends(JWTBearer())):
    response = CustomerService(db, user).get_record(id)
    return response


@customer_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData[CustomerResponseDTO],
)
def create(
    customer: CustomerDTO,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = CustomerService(db, user).create_record(customer)
    return response


@customer_router.put(
    "",
    response_model=ResponseData[CustomerResponseDTO],
)
def update(
    customer: CustomerDTO,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = CustomerService(db, user).update_record(customer, customer.customer_id)
    return response


@customer_router.delete(
    "/multiple",
    response_model=ResponseData[SuccessDTO],
)
async def delete_multiple(
    ids: List[int] = Query(...),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = CustomerService(db, user).delete_multiple(ids)
    return response


@customer_router.delete(
    "/{id}",
    response_model=ResponseData[SuccessDTO],
)
def delete(
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    response = CustomerService(db, user).delete_record(id)
    return response

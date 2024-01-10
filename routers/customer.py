from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm.session import Session

from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from models.user import User as UserModel
from schemas.customer import Customer, CustomerUpdate
from services.customer_service import CustomerService

customer_router = APIRouter()


@customer_router.get(
    "/api/customers",
    tags=["Customers"],
    status_code=200,
)
def get_customers(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    response = CustomerService(db, user).get_records(start, length, query)
    return response


@customer_router.get(
    "/api/customers/{id}",
    tags=["Customers"],
    status_code=200,
    response_model=Customer | dict,
)
def get_customer(
    id: int, db: Session = Depends(get_db), user: UserModel = Depends(JWTBearer())
):
    response = CustomerService(db, user).get_record(id)
    return response


@customer_router.post(
    "/api/customers",
    tags=["Customers"],
    status_code=201,
    response_model=Customer | dict,
)
def create_customer(
    customer: Customer,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    customer.customer_id = None
    user_id = user.user_id
    response = CustomerService(db, user).create_record(customer, user_id)
    return response


@customer_router.put(
    "/api/customers",
    tags=["Customers"],
    status_code=200,
    response_model=Customer | dict,
)
def update_customer(
    customer: CustomerUpdate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = CustomerService(db, user).update_record(
        customer, user_id, customer.customer_id
    )
    return response


@customer_router.delete(
    "/api/customers/multiple",
    tags=["Customers"],
    response_model=dict,
    status_code=200,
)
async def delete_multiple(
    ids: List[int] = Query(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = CustomerService(db, user).delete_multiple(ids, user_id)
    return response


@customer_router.delete(
    "/api/customers/{id}",
    tags=["Customers"],
    response_model=dict,
    status_code=200,
)
def delete_customer(
    id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = CustomerService(db, user).delete_record(id, user_id)
    return response

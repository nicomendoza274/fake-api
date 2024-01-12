from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm.session import Session

from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from models.user import User as UserModel
from schemas.customer import Customer, CustomerUpdate
from services.customer_service import CustomerService

customer_router = APIRouter(
    prefix="/api/customers",
    tags=["Customers"],
)


@customer_router.get("")
def list(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    response = CustomerService(db, user).get_records(start, length, query)
    return response


@customer_router.get("/{id}", response_model=Customer | dict)
def get(
    id: int, db: Session = Depends(get_db), user: UserModel = Depends(JWTBearer())
):
    response = CustomerService(db, user).get_record(id)
    return response


@customer_router.post("", status_code=201, response_model=Customer | dict)
def create(
    customer: Customer,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    customer.customer_id = None
    user_id = user.user_id
    response = CustomerService(db, user).create_record(customer, user_id)
    return response


@customer_router.put("", status_code=200, response_model=Customer | dict)
def update(
    customer: CustomerUpdate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = CustomerService(db, user).update_record(
        customer, user_id, customer.customer_id
    )
    return response


@customer_router.delete("/multiple", response_model=dict)
async def delete_multiple(
    ids: List[int] = Query(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = CustomerService(db, user).delete_multiple(ids, user_id)
    return response


@customer_router.delete("/{id}", response_model=dict)
def delete(
    id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    user_id = user.user_id
    response = CustomerService(db, user).delete_record(id, user_id)
    return response

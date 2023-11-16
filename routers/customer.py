from typing import List

from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.params import Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session

from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from models.user import User as UserModel
from schemas.customer import Customer, CustomerUpdate
from services.customer_service import CustomerService

customer_router = APIRouter()


@customer_router.get(
    "/api/customer",
    tags=["Customer"],
    status_code=200,
)
def get_customers(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    if not user:
        return Response(status_code=401)

    response = CustomerService(db).get_records(start, length, query)

    return JSONResponse(status_code=200, content=response)


@customer_router.get(
    "/api/customer/{id}",
    tags=["Customer"],
    status_code=200,
    response_model=Customer | dict,
)
def get_customer(
    id: int, db: Session = Depends(get_db), user: UserModel = Depends(JWTBearer())
):
    if not user:
        return Response(status_code=401)

    result = CustomerService(db=db).get_record(id)

    return CustomerService(db).response(result)


@customer_router.post(
    "/api/customer",
    tags=["Customer"],
    status_code=201,
    response_model=Customer | dict,
)
def create_customer(
    customer: Customer,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    if not user:
        return Response(status_code=401)

    customer.customer_id = None
    user_id = user.user_id
    result = CustomerService(db=db).create_record(customer, user_id)

    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@customer_router.put(
    "/api/customer",
    tags=["Customer"],
    status_code=200,
    response_model=Customer | dict,
)
def update_customer(
    customer: CustomerUpdate,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    if not user:
        return Response(status_code=401)

    user_id = user.user_id
    result = CustomerService(db=db).update_record(
        customer, user_id, customer.customer_id
    )

    return CustomerService(db).response(result)


@customer_router.delete(
    "/api/customer/multiple",
    tags=["Customer"],
    response_model=dict,
    status_code=200,
)
async def delete_multiple(
    ids: List[int] = Query(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    if not user:
        return Response(status_code=401)

    user_id = user.user_id
    result = CustomerService(db=db).delete_multiple(ids, user_id)

    return CustomerService(db).response(result)


@customer_router.delete(
    "/api/customer/{id}",
    tags=["Customer"],
    response_model=dict,
    status_code=200,
)
def delete_customer(
    id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(JWTBearer()),
):
    if not user:
        return Response(status_code=401)

    user_id = user.user_id
    result = CustomerService(db=db).delete_record(id, user_id)

    return CustomerService(db).response(result)

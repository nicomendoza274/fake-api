from typing import List

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.database import Session, get_db
from middlewares.jwt_bearer import JWTBearer
from models.user import User as UserModel
from schemas.customer import Customer
from services.customer_service import CustomerService

customer_router = APIRouter()


@customer_router.get(
    "/api/customer",
    tags=["customer"],
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
def get_customers(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
) -> List[Customer]:
    result = CustomerService(db).get_records(start, length, query)
    response = {
        "count": len(result),
        "start": start,
        "length": len(result) if length == 0 else length,
        "data": jsonable_encoder(result),
    }
    return JSONResponse(status_code=200, content=response)


@customer_router.get(
    "/api/customer/{id}",
    tags=["customer"],
    response_model=Customer,
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
def get_customer(id: int, db: Session = Depends(get_db)) -> Customer:
    result = CustomerService(db).get_record(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Not Found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@customer_router.post(
    "/api/customer",
    tags=["customer"],
    response_model=dict,
    status_code=201,
    dependencies=[Depends(JWTBearer())],
)
def create_customer(
    customer: Customer,
    user: UserModel = Depends(JWTBearer()),
    db: Session = Depends(get_db),
) -> dict:
    user_id = user.user_id
    result = CustomerService(db).create_record(customer, user_id)
    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@customer_router.put(
    "/api/customer/{id}",
    tags=["customer"],
    response_model=dict,
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
def update_customer(
    id: int,
    customer: Customer,
    user: UserModel = Depends(JWTBearer()),
    db: Session = Depends(get_db),
) -> dict:
    user_id = user.user_id
    result = CustomerService(db).get_record(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Not Found"})

    result = CustomerService(db).update_record(id, customer, user_id)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@customer_router.delete(
    "/api/customer/{id}",
    tags=["customer"],
    response_model=dict,
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
def delete_customer(
    id: int, user: UserModel = Depends(JWTBearer()), db: Session = Depends(get_db)
) -> dict:
    user_id = user.user_id
    result = CustomerService(db).get_record(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Not Found"})

    CustomerService(db).delete_record(id, user_id)
    return JSONResponse(content={"message": "deleted"})

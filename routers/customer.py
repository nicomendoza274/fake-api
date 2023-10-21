from typing import List

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from schemas.customer import Customer
from services.customer_service import CustomerService
from utils.jwt_manager import get_user_id

customer_router = APIRouter()


@customer_router.get(
    "/api/customer",
    tags=["customer"],
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
def get_customers(
    start: int | None = 0, length: int | None = 15, query: str | None = None
) -> List[Customer]:
    db = Session()
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
def get_customer(id: int) -> Customer:
    db = Session()
    result = CustomerService(db).get_record(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@customer_router.post(
    "/api/customer",
    tags=["customer"],
    response_model=dict,
    status_code=201,
    dependencies=[Depends(JWTBearer())],
)
async def create_customer(customer: Customer, req: Request) -> dict:
    user_id = await get_user_id(req)
    db = Session()
    result = CustomerService(db).create_record(customer, user_id)
    print(result)
    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@customer_router.put(
    "/api/customer/{id}",
    tags=["customer"],
    response_model=dict,
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
async def update_customer(id: int, customer: Customer, req: Request) -> dict:
    user_id = await get_user_id(req)
    db = Session()
    result = CustomerService(db).get_record(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})

    result = CustomerService(db).update_record(id, customer, user_id)
    print(jsonable_encoder(result))
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@customer_router.delete(
    "/api/customer/{id}",
    tags=["customer"],
    response_model=dict,
    status_code=200,
    dependencies=[Depends(JWTBearer())],
)
async def delete_customer(id: int, req: Request) -> dict:
    user_id = await get_user_id(req)
    db = Session()
    result = CustomerService(db).get_record(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})

    CustomerService(db).delete_record(id, user_id)
    return JSONResponse(content={"message": "ok"})

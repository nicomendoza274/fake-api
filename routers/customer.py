from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from config.database import Session
from typing import List
from middlewares.jwt_bearer import JWTBearer
from schemas.customer import Customer
from services.customer_service import CustomerService
from models.customer import Customer as CustomerModel

customer_router = APIRouter()


@customer_router.get('/api/customer', tags=['customer'], response_model=List[Customer], status_code=200, dependencies=[Depends(JWTBearer())])
def get_customers() -> List[Customer]:
    db = Session()
    result = CustomerService(db).get_records()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@customer_router.get('/api/customer/{id}', tags=['customer'], response_model=Customer, status_code=200)
def get_customer(id: int) -> Customer:
    db = Session()
    result = CustomerService(db).get_record(id)
    if not result:
        return JSONResponse(status_code=404, content={'message' : "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@customer_router.post('/api/customer', tags=['customer'], response_model=dict, status_code=201)
def create_customer(customer: Customer) -> dict:
    db = Session()
    result = CustomerService(db).create_record(customer)
    print(result)
    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@customer_router.put('/api/customer/{id}', tags=['customer'], response_model=dict, status_code=200)
def update_customer(id: int, customer: Customer) -> dict:
    db = Session()
    result = CustomerService(db).get_record(id)
    if not result:
        return JSONResponse(status_code=404, content={'message' : "No encontrado"})

    result = CustomerService(db).update_record(id, customer)
    print(jsonable_encoder(result))
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@customer_router.delete('/api/customer/{id}', tags=['customer'], response_model=dict, status_code=200)
def delete_customer(id: int) -> dict:
    db = Session()
    result = CustomerService(db).get_record(id)
    if not result:
        return JSONResponse(status_code=404, content={'message' : "No encontrado"})

    CustomerService(db).delete_record(id)
    return JSONResponse(content={"message" : "ok"})
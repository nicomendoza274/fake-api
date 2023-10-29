from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session

from config.database import get_db
from middlewares.jwt_bearer import JWTBearer
from models.user import User as UserModel
from schemas.customer import CuastomerUpdate, Customer
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
):
    response = CustomerService(db=db).get_records(start, length, query)
    return JSONResponse(status_code=200, content=response)


@customer_router.get(
    "/api/customer/{id}",
    tags=["customer"],
    status_code=200,
    response_model=Customer | dict,
    dependencies=[Depends(JWTBearer())],
)
def get_customer(id: int, db: Session = Depends(get_db)):
    result = CustomerService(db=db).get_record(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Not Found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@customer_router.post(
    "/api/customer",
    tags=["customer"],
    status_code=201,
    response_model=Customer | dict,
    dependencies=[Depends(JWTBearer())],
)
def create_customer(
    customer: Customer,
    user: UserModel = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    customer.customer_id = None
    user_id = user.user_id
    result = CustomerService(db=db).create_record(customer, user_id)
    return JSONResponse(status_code=201, content=jsonable_encoder(result))


@customer_router.put(
    "/api/customer",
    tags=["customer"],
    status_code=200,
    response_model=Customer | dict,
    dependencies=[Depends(JWTBearer())],
)
def update_customer(
    customer: CuastomerUpdate,
    user: UserModel = Depends(JWTBearer()),
    db: Session = Depends(get_db),
):
    user_id = user.user_id
    result = CustomerService(db=db).update_record(
        customer, user_id, customer.customer_id
    )
    if not result:
        return JSONResponse(status_code=404, content={"message": "Not Found"})
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
):
    user_id = user.user_id

    result = CustomerService(db=db).delete_record(id, user_id)

    if not result:
        return JSONResponse(status_code=404, content={"message": "Not Found"})

    return JSONResponse(content=result)

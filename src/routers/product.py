from fastapi import APIRouter, Depends, Form, Path, Request, status

from core.constants.responses import NOT_200, NOT_201, NOT_422
from core.database.database import SessionDep
from core.models.response import MultipleResponseData, ResponseData
from core.models.toggle import ActiveToggleDTO
from core.services.file import FileService
from core.utils.json_validate import validate_json_data
from core.utils.query import str_to_query
from core.utils.response import get_empty_response, get_multiple_response, get_response
from middlewares.jwt_bearer import JWTBearer
from models.product import CreateProductDTO, Product, ProductDTO, ProductResponseDTO
from models.user import User
from services.product import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get(
    path="",
    response_model=MultipleResponseData[ProductResponseDTO],
    responses=NOT_422,
)
def list_data(
    session: SessionDep,
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    user: User = Depends(JWTBearer()),
):
    query_criteria = str_to_query(query)
    product_list, total_count = ProductService(session, user).get_records(
        start, length, query_criteria
    )
    response = get_multiple_response(
        count=total_count,
        start=start,
        length=len(product_list) if length == 0 else length,
        data=product_list,
    )
    return response


@router.get(
    path="/{productId}",
    response_model=ResponseData[ProductResponseDTO],
    responses=NOT_422,
)
def get_data(
    session: SessionDep,
    product_id: int = Path(alias="productId"),
    user: User = Depends(JWTBearer()),
):
    product_data = ProductService(session, user).get_record(product_id)
    response = get_response(product_data)
    return response


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
    responses=NOT_422 | NOT_201,
)
def create_data(
    session: SessionDep,
    request: Request,
    body: CreateProductDTO = Form(..., media_type="multipart/form-data"),
    user: User = Depends(JWTBearer()),
):
    """
    Parameters
    ----------
    * **data**: This is a stringify object of product, for example:

        ```json
        {
            "categoryId": 0,
            "name": "string"
            "price": 0,
            "isActive": true,
            "pictureId": 0
        }
        ```

    * **picture**: This is an image file
    """

    product = validate_json_data(ProductDTO, body.data)
    new_file = FileService(session, user).save_file(body.picture, request)
    product.picture_id = new_file.file_id if new_file else None
    ProductService(session, user).create_record(product)
    response = get_empty_response(status.HTTP_201_CREATED)
    return response


@router.put(
    path="/{productId}",
    response_model=None,
    responses=NOT_422 | NOT_200,
)
def update_data(
    session: SessionDep,
    request: Request,
    body: CreateProductDTO = Form(..., media_type="multipart/form-data"),
    product_id: int = Path(alias="productId"),
    user: User = Depends(JWTBearer()),
):
    """
    Parameters
    ----------
    * **data**: This is a stringify object of product, for example:

        ```json
        {
            "categoryId": 0,
            "name": "string",
            "price": 0,
            "isActive": true,
            "pictureId": 0
        }
        ```

    * **picture**: This is an image file
    """

    product = validate_json_data(ProductDTO, body.data)

    if not product.picture_id:
        FileService(session, user).delete_file(
            Product, product.product_id, "picture_id"
        )
        new_file = FileService(session, user).save_file(body.picture, request)
        product.file_id = new_file.file_id if new_file else None
    ProductService(session, user).update_record(product, product_id)
    response = get_empty_response()
    return response


@router.put(
    path="/activate/{productId}",
    response_model=None,
    responses=NOT_422 | NOT_200,
)
def toggle_active(
    session: SessionDep,
    data: ActiveToggleDTO,
    product_id: int = Path(alias="productId"),
    user: User = Depends(JWTBearer()),
):
    ProductService(session, user).toggle_active(data, product_id)
    response = get_empty_response()
    return response


@router.delete(
    path="/{productId}",
    response_model=None,
    responses=NOT_422 | NOT_200,
)
def delete_data(
    session: SessionDep,
    product_id: int = Path(alias="productId"),
    user: User = Depends(JWTBearer()),
):
    ProductService(session, user).delete_record(product_id)
    response = get_empty_response()
    return response

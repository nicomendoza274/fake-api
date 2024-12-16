from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Path,
    Query,
    Request,
    UploadFile,
    status,
)
from sqlalchemy.orm.session import Session

from core.database.database import get_db
from core.schemas.active_toggle import ActiveToggleDTO
from core.schemas.response import MultipleResponseData, ResponseData
from core.services.file import FileService
from core.utils.json_validate import validate_json_data
from core.utils.query import str_to_query
from core.utils.response import get_empty_response, get_multiple_response, get_response
from middlewares.jwt_bearer import JWTBearer
from models.models import Product, User
from schemas.product import ProductDTO, ProductResponseDTO
from services.product import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get(
    "",
    response_model=MultipleResponseData[list[ProductResponseDTO]],
)
def list_data(
    start: int | None = 0,
    length: int | None = 15,
    query: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    query_criteria = str_to_query(query)
    product_list, total_count = ProductService(db, user).get_records(
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
    "/{productId}",
    response_model=ResponseData[ProductResponseDTO],
)
def get(
    product_id: int = Path(alias="productId"),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    product_data = ProductService(db, user).get_record(product_id)
    response = get_response(product_data)
    return response


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
def create(
    request: Request,
    json_data: str = Form(
        ...,
        alias="application/json",
        validation_alias="application/json",
    ),
    picture: UploadFile = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    """
    Parameters
    ----------
    * **application/json**: This is a stringify object of product, for example:

        ```json
        {
            categoryId: 0
            name: "string"
            price: 0
            isActive: "boolean"
            fileId: 0
        }```

    * **picture**: This is an image file
    """

    product = validate_json_data(ProductDTO, json_data)
    new_file = FileService(db, user).save_file(picture, request)
    product.file_id = new_file.file_id if new_file else None
    ProductService(db, user).create_record(product)
    response = get_empty_response(status.HTTP_201_CREATED)
    return response


@router.put(
    "/{productId}",
    response_model=None,
)
def update(
    request: Request,
    product_id: int = Path(alias="productId"),
    json_data: str = Form(
        ...,
        alias="application/json",
        validation_alias="application/json",
    ),
    picture: UploadFile = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    """
    Parameters
    ----------
    * **application/json**: This is a stringify object of product, for example:

        ```json
        {
            productId: 0
            categoryId: 0
            name: "string"
            price: 0
            isActive: "boolean"
            fileId: 0
        }```

    * **picture**: This is an image file
    """

    product = validate_json_data(ProductDTO, json_data)

    if not product.file_id:
        FileService(db, user).delete_file(Product, product.product_id, "picture_id")
        new_file = FileService(db, user).save_file(picture, request)
        product.file_id = new_file.file_id if new_file else None
    ProductService(db, user).update_record(product, product_id)
    response = get_empty_response()
    return response


@router.put(
    "/activate/{productId}",
    response_model=None,
)
def toggle_active(
    data: ActiveToggleDTO,
    product_id: int = Path(alias="productId"),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    ProductService(db, user).toggle_active(data, product_id)
    response = get_empty_response()
    return response


@router.delete(
    "/multiple",
    response_model=None,
)
async def delete_multiple(
    ids: list[int] = Query(...),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    ProductService(db, user).delete_multiple(ids)
    response = get_empty_response()
    return response


@router.delete(
    "/{productId}",
    response_model=None,
)
def delete(
    product_id: int = Path(alias="productId"),
    db: Session = Depends(get_db),
    user: User = Depends(JWTBearer()),
):
    ProductService(db, user).delete_record(product_id)
    response = get_empty_response()
    return response

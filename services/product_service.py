from typing import Callable

from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import desc, inspect
from sqlalchemy.orm.session import Session

from classes.query import Query
from models.category import Category as CategoryModel
from models.product import Product as ProductModel
from models.user import User as UserModel
from schemas.category import Category, CategoryUpdate
from schemas.product import Product, ProductCategory
from services.base_service import BaseService
from utils.encrypt import base64_decode
from utils.json_manager import json_parse
from utils.snake_case import to_snake_case


class ProductService(BaseService):
    def __init__(self, db: Session, user: UserModel) -> None:
        self.db = db
        self.current_user = user
        self.sqlModel = ProductModel
        self.model = Product

    def get_records(self, start: int | None, length: int | None, query: str | None):
        if not self.current_user:
            return Response(status_code=401)

        model = (
            self.db.query(ProductModel, CategoryModel)
            .join(
                CategoryModel,
                ProductModel.category_id == CategoryModel.category_id,
                isouter=True,
            )
            .filter(ProductModel.deleted_at == None)
        )

        pk = inspect(ProductModel).primary_key[0].name

        if query:
            json_query = base64_decode(query)
            json = json_parse(json_query)
            json = {key.lower(): value for key, value in json.items()}

            if "sorts" in json and len(json["sorts"]) > 0:
                for sort in json["sorts"]:
                    property_name = to_snake_case(sort["propertyName"])
                    descending = sort["descending"]

                    if descending == False:
                        if property_name == "category.name":
                            model = model.order_by(CategoryModel.name)
                        else:
                            model = model.order_by(property_name)
                    else:
                        if property_name == "category.name":
                            model = model.order_by(desc(CategoryModel.name))
                        else:
                            model = model.order_by(desc(property_name))

            if "filters" in json and len(json["filters"]) > 0:
                model = Query(model, self.sqlModel).filters(json)

            if "search" in json:
                model = Query(model, self.sqlModel).search(json, "name")

        model = model.order_by(pk)
        total_count = len(model.all())

        if length:
            model = model.limit(length)

        if start:
            model = model.offset(start)

        result = model.all()

        map_product_category: Callable[
            [Product, Category], ProductCategory
        ] = lambda product, category: ProductCategory(
            product_id=product.product_id,
            category_id=product.category_id,
            name=product.name,
            price=product.price,
            category=(
                CategoryUpdate(category_id=category.category_id, name=category.name)
                if product.category_id
                else None
            ),
            is_active=product.is_active,
            created_at=product.created_at,
            created_by=product.created_by,
            updated_at=product.updated_at,
            updated_by=product.updated_by,
            deleted_at=product.deleted_at,
            deleted_by=product.deleted_by,
        )

        entity = [map_product_category(el[0], el[1]) for el in result]

        response = {
            "count": total_count,
            "start": start,
            "length": len(entity) if length == 0 else length,
            "data": jsonable_encoder(entity),
        }

        return JSONResponse(status_code=200, content=response)

    def get_record(self, id: int):
        if not self.current_user:
            return Response(status_code=401)

        model = (
            self.db.query(ProductModel, CategoryModel)
            .join(
                CategoryModel,
                ProductModel.category_id == CategoryModel.category_id,
                isouter=True,
            )
            .filter(ProductModel.product_id == id)
            .first()
        )

        if not model:
            return Response(status_code=401)

        product = model[0]
        category = model[1]

        result = ProductCategory(
            product_id=product.product_id,
            category_id=product.category_id,
            name=product.name,
            price=product.price,
            category=(
                CategoryUpdate(category_id=category.category_id, name=category.name)
                if product.category_id
                else None
            ),
            is_active=product.is_active,
            created_at=product.created_at,
            created_by=product.created_by,
            updated_at=product.updated_at,
            updated_by=product.updated_by,
            deleted_at=product.deleted_at,
            deleted_by=product.deleted_by,
        )

        if not result or result.deleted_at != None:
            return self.response(None)

        entity = jsonable_encoder(result)
        response = self.response(entity)

        return response

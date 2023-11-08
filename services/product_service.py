from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc, func, inspect
from sqlalchemy.orm.session import Session

from classes.query import Query
from models.category import Category as CategoryModel
from models.product import Product as ProductModel
from schemas.category import Category, CategoryUpdate
from schemas.product import Product, ProductCategory
from services.base_service import BaseService
from utils.encrypt import base64_decode
from utils.json_manager import json_parse
from utils.snake_case import to_snake_case


class ProductService(BaseService):
    def __init__(self, db: Session) -> None:
        self.db = db
        self.sqlModel = ProductModel
        self.model = Product

    def get_records(self, start: int | None, length: int | None, query: str | None):
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

        entity = []
        for el in result:
            product: Product = el[0]
            category: Category = el[1]
            product_category = ProductCategory(
                product_id=product.product_id,
                category_id=product.category_id,
                name=product.name,
                price=product.price,
                category=None,
                is_active=product.is_active,
                created_at=product.created_at,
                created_by=product.created_by,
                updated_at=product.updated_at,
                updated_by=product.updated_by,
                deleted_at=product.deleted_at,
                deleted_by=product.deleted_by,
            )

            if product.category_id:
                product_category.category = CategoryUpdate(
                    category_id=category.category_id, name=category.name
                )

            entity.append(product_category)

        response = {
            "count": total_count,
            "start": start,
            "length": len(result[0]) if length == 0 else length,
            "data": jsonable_encoder(entity),
        }

        return response

    def delete_records(self, ids: List[int], user_id: int):
        for id in ids:
            result = self.db.query(self.sqlModel).get(id)

            if not result or result.deleted_at != None:
                break

            result.deleted_at = func.now()
            result.deleted_by = user_id

        self.db.commit()
        return {"message": "deleted"}

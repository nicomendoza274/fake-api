from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc, func
from sqlalchemy.orm.session import Session

from models.product import Product as ProductModel
from schemas.product import Product
from utils.encrypt import base64_decode
from utils.json_manager import json_parse
from utils.snake_case import to_snake_case


class ProductService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_records(self, start: int | None, length: int | None, query: str | None):
        model = self.db.query(ProductModel).filter(ProductModel.deleted_at == None)
        if query:
            json_query = base64_decode(query)
            json = json_parse(json_query)
            json = {key.lower(): value for key, value in json.items()}

            if "sorts" in json and len(json["sorts"]) > 0:
                for sort in json["sorts"]:
                    property_name = to_snake_case(sort["propertyName"])
                    descending = sort["descending"]

                    if descending == False:
                        model = model.order_by(property_name)
                    else:
                        model = model.order_by(desc(property_name))

            if "filters" in json and len(json["filters"]) > 0:
                for filter in json["filters"]:
                    property_name = to_snake_case(filter["propertyName"])
                    type_filer = filter["type"]
                    value_filter = filter["value"]

                    if type_filer == "eq":
                        model = model.filter(
                            getattr(ProductModel, property_name) == value_filter
                        )
                    elif type_filer == "neq":
                        model = model.filter(
                            getattr(ProductModel, property_name) != value_filter
                        )
                    elif type_filer == "gt":
                        model = model.filter(
                            getattr(ProductModel, property_name) > value_filter
                        )
                    elif type_filer == "lt":
                        model = model.filter(
                            getattr(ProductModel, property_name) < value_filter
                        )
                    elif type_filer == "gte":
                        model = model.filter(
                            getattr(ProductModel, property_name) >= value_filter
                        )
                    elif type_filer == "lte":
                        model = model.filter(
                            getattr(ProductModel, property_name) <= value_filter
                        )
                    elif type_filer == "like":
                        search = "%{}%".format(value_filter)
                        model = model.filter(
                            getattr(ProductModel, property_name).like(search)
                        )
                    elif type_filer == "contains":
                        search = "%{}%".format(value_filter)
                        model = model.filter(
                            getattr(ProductModel, property_name).like(search)
                        )

            if "search" in json:
                search = json["search"]
                search = "%{}%".format(search)
                model = model.filter(getattr(ProductModel, "name").ilike(search))

        total_count = len(model.all())

        if length:
            model = model.limit(length)

        if start:
            model = model.offset(start)

        result = model.all()
        products = [Product.model_validate(jsonable_encoder(el)) for el in result]

        response = {
            "count": total_count,
            "start": start,
            "length": len(result) if length == 0 else length,
            "data": jsonable_encoder(products),
        }

        return response

    def get_record(self, id: int):
        result = (
            self.db.query(ProductModel)
            .filter(ProductModel.deleted_at == None, ProductModel.product_id == id)
            .first()
        )

        if not result:
            return None

        response = Product.model_validate(jsonable_encoder(result))
        return response

    def create_record(self, data: Product, user_id: int):
        new_record = ProductModel(**data.model_dump())
        new_record.created_by = user_id
        new_record.product_id = None
        self.db.add(new_record)
        self.db.commit()
        self.db.refresh(new_record)
        response = Product.model_validate(jsonable_encoder(new_record))
        return response

    def update_record(self, data: Product, user_id: int):
        result: ProductModel = (
            self.db.query(ProductModel)
            .filter(
                ProductModel.deleted_at == None,
                ProductModel.product_id == data.product_id,
            )
            .first()
        )

        if not result:
            return None

        result.name = data.name
        result.price = data.price
        result.updated_by = user_id
        result.updated_at = func.now()

        self.db.commit()
        self.db.refresh(result)
        response = Product.model_validate(jsonable_encoder(result))
        return response

    def delete_record(self, id: int, user_id: int):
        response: ProductModel = (
            self.db.query(ProductModel)
            .filter(ProductModel.deleted_at == None, ProductModel.product_id == id)
            .first()
        )

        if not response:
            return None

        response.deleted_at = func.now()
        response.deleted_by = user_id
        self.db.commit()
        return {"message": "deleted"}

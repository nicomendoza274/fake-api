from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm.session import Session

from classes.query import Query
from utils.encrypt import base64_decode
from utils.json_manager import json_parse


class BaseService:
    def __init__(self, db: Session, schema, model) -> None:
        self.db = db
        self.schema = schema
        self.model = model

    def get_records(self, start: int | None, length: int | None, query: str | None):
        model = self.db.query(self.schema).filter(self.schema.deleted_at == None)
        if query:
            json_query = base64_decode(query)
            json = json_parse(json_query)
            json = {key.lower(): value for key, value in json.items()}

            if "sorts" in json and len(json["sorts"]) > 0:
                model = Query(model, self.schema).sorts(json)

            if "filters" in json and len(json["filters"]) > 0:
                model = Query(model, self.schema).filters(json)

            if "search" in json:
                model = Query(model, self.schema).search(json, "name")

        total_count = len(model.all())

        if length:
            model = model.limit(length)

        if start:
            model = model.offset(start)

        result = model.all()
        entity = [self.model.model_validate(jsonable_encoder(el)) for el in result]

        response = {
            "count": total_count,
            "start": start,
            "length": len(result) if length == 0 else length,
            "data": jsonable_encoder(entity),
        }

        return response

    def get_record(self, id: int):
        result = self.db.query(self.schema).get(id)

        if result.deleted_at != None:
            return None

        if not result:
            return None

        customer = self.model.model_validate(jsonable_encoder(result))
        return customer

    def create_record(self, data, user_id: int):
        new_record = self.schema(**data.model_dump())
        new_record.created_by = user_id
        self.db.add(new_record)
        self.db.commit()
        self.db.refresh(new_record)
        entity = self.model.model_validate(jsonable_encoder(new_record))
        return entity

    def update_record(self, data, user_id: int, id: int):
        result = self.db.query(self.schema).get(id)

        if result.deleted_at != None:
            return None

        if not result:
            return None

        model_to_dict = data.model_dump()

        for key, value in model_to_dict.items():
            setattr(result, key, value)

        result.updated_by = user_id
        result.updated_at = func.now()

        self.db.commit()
        self.db.refresh(result)
        entity = self.model.model_validate(jsonable_encoder(result))
        return entity

    def delete_record(self, id: int, user_id: int):
        result = self.db.query(self.schema).get(id)

        if result.deleted_at != None:
            return None

        if not result:
            return None

        result.deleted_at = func.now()
        result.deleted_by = user_id
        self.db.commit()
        return {"message": "deleted"}

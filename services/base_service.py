from fastapi.encoders import jsonable_encoder

from classes.query import Query
from utils.encrypt import base64_decode
from utils.json_manager import json_parse


class BaseService:
    # def __init__(self, db, model) -> None:
    #     self.db = db
    #     self.model = model

    def get_records(self, start: int | None, length: int | None, query: str | None):
        model = self.db.query(self.model).filter(self.model.deleted_at == None)
        if query:
            json_query = base64_decode(query)
            json = json_parse(json_query)
            json = {key.lower(): value for key, value in json.items()}

            if "sorts" in json and len(json["sorts"]) > 0:
                model = Query(model, self.model).sorts(json)

            if "filters" in json and len(json["filters"]) > 0:
                model = Query(model, self.model).filters(json)

            if "search" in json:
                model = Query(model, self.model).search(json, "name")

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
        result = self.db.query(self.model).filter(self.model.id == id).first()
        return result

    def create_record(self, data):
        new_record = self.model(**data.model_dump())
        self.db.add(new_record)
        self.db.commit()
        return

    def update_record(self, id: int, data):
        # record = self.db.query(self.Model).filter(self.Model.id == id).first()
        self.db.update(id, data)
        self.db.commit()
        return

    def delete_record(self, id: int):
        result = self.db.query(self.model).filter(self.model.id == id).first()
        self.db.delete(result)
        self.db.commit()
        return

from typing import List

from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import func, inspect
from sqlalchemy.orm.session import Session

from classes.query import Query
from constants.error import GEN_4000
from models.user import User as UserModel
from schemas.error import Errors
from utils.encrypt import base64_decode
from utils.json_manager import json_parse


class BaseService:
    def __init__(self, db: Session, current_user: UserModel, sqlModel, model) -> None:
        self.db = db
        self.current_user = current_user
        self.sqlModel = sqlModel
        self.model = model

    def get_records(self, start: int | None, length: int | None, query: str | None):
        if not self.current_user:
            return Response(status_code=401)

        model = self.db.query(self.sqlModel).filter(self.sqlModel.deleted_at == None)
        pk = inspect(self.sqlModel).primary_key[0].name

        if query:
            json_query = base64_decode(query)
            json = json_parse(json_query)
            json = {key.lower(): value for key, value in json.items()}

            if "sorts" in json and len(json["sorts"]) > 0:
                model = Query(model, self.sqlModel).sorts(json)

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
        entity = [self.model.model_validate(jsonable_encoder(el)) for el in result]

        response = {
            "count": total_count,
            "start": start,
            "length": len(result) if length == 0 else length,
            "data": jsonable_encoder(entity),
        }

        return JSONResponse(status_code=200, content=response)

    def get_record(self, id: int):
        if not self.current_user:
            return Response(status_code=401)

        result = self.db.query(self.sqlModel).get(id)

        if not result or result.deleted_at != None:
            return self.response(None)

        entity = self.model.model_validate(jsonable_encoder(result))
        response = self.response(entity)

        return response

    def create_record(self, data, user_id: int):
        if not self.current_user:
            return Response(status_code=401)

        new_record = self.sqlModel(**data.model_dump())
        new_record.created_by = user_id
        self.db.add(new_record)
        self.db.commit()
        self.db.refresh(new_record)
        response = self.model.model_validate(jsonable_encoder(new_record))
        response = {"data": response}

        return JSONResponse(status_code=201, content=jsonable_encoder(response))

    def update_record(self, data, user_id: int, id: int):
        if not self.current_user:
            return Response(status_code=401)

        result = self.db.query(self.sqlModel).get(id)

        if not result or result.deleted_at != None:
            return None

        model_to_dict = data.model_dump()

        for key, value in model_to_dict.items():
            setattr(result, key, value)

        result.updated_by = user_id
        result.updated_at = func.now()

        self.db.commit()
        self.db.refresh(result)
        entity = self.model.model_validate(jsonable_encoder(result))
        response = self.response(entity)
        return response

    def tooggle_active(self, data, user_id: int, id: int):
        if not self.current_user:
            return Response(status_code=401)

        result = self.db.query(self.sqlModel).get(id)

        if not result or result.deleted_at != None:
            return None

        result.is_active = data.is_active
        result.updated_by = user_id
        result.updated_at = func.now()

        self.db.commit()
        self.db.refresh(result)

        entity = self.model.model_validate(jsonable_encoder(result))
        response = self.response(entity)
        return response

    def delete_multiple(self, ids: List[int], user_id: int):
        if not self.current_user:
            return Response(status_code=401)

        for id in ids:
            result = self.db.query(self.sqlModel).get(id)

            if result and result.deleted_at == None:
                result.deleted_at = func.now()
                result.deleted_by = user_id

        self.db.commit()

        response = self.response({"message": "deleted"})
        return response

    def delete_record(self, id: int, user_id: int):
        if not self.current_user:
            return Response(status_code=401)

        result = self.db.query(self.sqlModel).get(id)

        if not result or result.deleted_at != None:
            return self.response(None)

        result.deleted_at = func.now()
        result.deleted_by = user_id
        self.db.commit()

        response = self.response({"message": "deleted"})
        return response

    def response(self, result):
        if not result:
            content = Errors(Errors=[GEN_4000]).model_dump()

            return JSONResponse(status_code=404, content=content)

        result = {"data": result}
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

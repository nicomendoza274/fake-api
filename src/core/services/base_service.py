from typing import List

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import func, inspect
from sqlalchemy.orm.session import Session

from core.classes.generic_errors import GenericError
from core.constants.generic_errors import GEN_4000
from core.models.user import UserModel
from core.schemas.response import MultipleResponseData, ResponseData
from core.schemas.success_schema import SuccessDTO
from core.services.query import QueryCriterionService
from core.utils.query import str_to_query


class BaseService:
    def __init__(
        self, db: Session, current_user: UserModel | None, sqlModel, response_schema
    ) -> None:
        self.db = db
        self.current_user = current_user
        self.sqlModel = sqlModel
        self.response_schema = response_schema

    def get_records(self, start: int | None, length: int | None, query: str | None):
        result = self.db.query(self.sqlModel).filter(self.sqlModel.deleted_at == None)
        pk = inspect(self.sqlModel).primary_key[0].name

        query_model = QueryCriterionService(self.sqlModel)

        query_criteria = str_to_query(query)

        result = query_model.sorts(query_criteria, result)
        result = query_model.filters(query_criteria, result)
        result = query_model.search(query_criteria, "name", result)

        result = result.order_by(pk)
        total_count = len(result.all())

        if length:
            result = result.limit(length)

        if start:
            result = result.offset(start)

        result = result.all()
        data_response_list = [self.response_schema.model_validate(el) for el in result]

        response = self.get_multiple_response(
            count=total_count,
            start=start,
            length=len(result) if length == 0 else length,
            data=data_response_list,
        )

        return response

    def get_record(self, id: int):
        result = self.db.query(self.sqlModel).get(id)

        if not result or result.deleted_at != None:
            raise GenericError(GEN_4000)

        data_response = self.response_schema.model_validate(result)
        response = self.get_response(data_response)

        return response

    def create_record(self, data):
        new_record = self.sqlModel(**data.model_dump())
        if self.current_user:
            new_record.created_by = self.current_user.user_id
        self.db.add(new_record)
        self.db.flush()
        self.db.refresh(new_record)
        data_response = self.response_schema.model_validate(new_record)

        response = self.get_response(data_response, status.HTTP_201_CREATED)
        self.db.commit()
        return response

    def update_record(self, data, id: int | None):

        result = self.db.query(self.sqlModel).get(id)

        if not result or result.deleted_at != None:
            raise GenericError(GEN_4000)

        model_to_dict = data.model_dump()

        for key, value in model_to_dict.items():
            setattr(result, key, value)

        if self.current_user:
            result.updated_by = self.current_user.user_id
        result.updated_at = func.now()

        self.db.flush()
        self.db.refresh(result)
        data_response = self.response_schema.model_validate(result)

        response = self.get_response(data_response)
        self.db.commit()
        return response

    def toggle_active(self, data, id: int):
        result = self.db.query(self.sqlModel).get(id)

        if not result or result.deleted_at != None:
            raise GenericError(GEN_4000)

        result.is_active = data.is_active
        if self.current_user:
            result.updated_by = self.current_user.user_id
        result.updated_at = func.now()
        self.db.flush()
        self.db.refresh(result)

        data_response = self.response_schema.model_validate(result)
        response = self.get_response(data_response)
        self.db.commit()
        return response

    def delete_multiple(self, ids: List[int]):
        for id in ids:
            result = self.db.query(self.sqlModel).get(id)

            if result and result.deleted_at == None:
                result.deleted_at = func.now()
                if self.current_user:
                    result.deleted_by = self.current_user.user_id

        response = self.get_response(SuccessDTO())
        self.db.commit()
        return response

    def delete_record(self, id: int):
        result = self.db.query(self.sqlModel).get(id)

        if not result or result.deleted_at != None:
            raise GenericError(GEN_4000)

        result.deleted_at = func.now()
        if self.current_user:
            result.deleted_by = self.current_user.user_id

        response = self.get_response(SuccessDTO())

        self.db.commit()
        return response

    def get_response(self, data, status_code=status.HTTP_200_OK):
        response = jsonable_encoder(ResponseData(data=data))
        return JSONResponse(status_code=status_code, content=response)

    def get_multiple_response(
        self,
        count: int,
        start: int | None,
        length: int | None,
        data,
        status_code=status.HTTP_200_OK,
    ):
        response = jsonable_encoder(
            MultipleResponseData(
                count=count,
                start=start,
                length=length,
                data=data,
            )
        )
        return JSONResponse(status_code=status_code, content=response)

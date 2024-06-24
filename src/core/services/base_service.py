from typing import List

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import func, inspect
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session

from core.classes.generic_errors import GenericError
from core.constants.generic_errors import GEN_4000
from core.models.user import UserModel
from core.schemas.query import PropertyModel
from core.schemas.response import MultipleResponseData, ResponseData
from core.schemas.success_schema import SuccessDTO
from core.services.query import QueryCriterionService


class BaseService:
    def __init__(
        self,
        db: Session,
        current_user: UserModel | None,
        sqlModel,
        response_schema,
    ) -> None:
        self.db = db
        self.current_user = current_user
        self.sqlModel = sqlModel
        self.response_schema = response_schema
        self.result = self.db.query(self.sqlModel)
        self.default_sort = inspect(self.sqlModel).primary_key[0].name  # PK
        self.property_model_list: List[PropertyModel] = []
        self.property_search = [getattr(self.sqlModel, "name")] if hasattr(self.sqlModel, "name") else []

    def get_records(self, start: int | None, length: int | None, query: str | None):
        result = self.result

        query_model = QueryCriterionService(self.sqlModel, query)

        result = self.filter_list(query_model, result)
        result = self.search_list(query_model, result)
        result = self.sort_list(query_model, result)
        result = self.sort_by_pk(result)

        if length:
            result = result.limit(length)

        if start:
            result = result.offset(start)

        result = result.all()
        total_count = len(result)

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

    def filter_list(self, query_model: QueryCriterionService, result: Query) -> Query:
        result = result.filter(self.sqlModel.deleted_at == None)
        return query_model.filters(result, self.property_model_list)

    def search_list(self, query_model: QueryCriterionService, result: Query) -> Query:
        return query_model.search(result, self.property_search)

    def sort_list(self, query_model: QueryCriterionService, result: Query) -> Query:
        return query_model.sorts(result, self.property_model_list)

    def sort_by_pk(self, result: Query) -> Query:
        return result.order_by(self.default_sort)

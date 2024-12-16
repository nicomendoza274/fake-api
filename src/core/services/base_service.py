from typing import Generic, Type, TypeVar

from fastapi import status
from sqlalchemy import func, inspect
from sqlalchemy.orm.query import Query

from core.classes.handle_exception import HandleException
from core.constants.generic_errors import GEN_4000
from core.database.database import SessionDep
from core.models.base import BaseAuditModel
from core.models.user import UserModel
from core.schemas.active_toggle import ActiveToggleDTO
from core.schemas.camel import CamelModel
from core.schemas.query import PropertyModel, QueryCriteria
from core.services.query import QueryCriterionService

T = TypeVar("T", bound=BaseAuditModel)
K = TypeVar("K", bound=CamelModel)
W = TypeVar("W", bound=CamelModel)


class BaseService(Generic[T, K, W]):
    def __init__(
        self,
        session: SessionDep,
        current_user: UserModel | None,
        sqlModel: Type[T],
        response_schema: Type[K] | None = None,
    ) -> None:
        self.session = session
        self.current_user = current_user
        self.sqlModel = sqlModel
        self.response_schema = response_schema
        self.result = self.session.query(self.sqlModel)
        self.default_sort = inspect(self.sqlModel).primary_key[0].name  # PK
        self.property_model_list: list[PropertyModel] = []
        self.property_search = (
            [getattr(self.sqlModel, "name")] if hasattr(self.sqlModel, "name") else []
        )

    def get_records(
        self,
        start: int | None,
        length: int | None,
        query_criteria: QueryCriteria | None,
    ) -> tuple[list[K], int]:
        if not self.response_schema:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        result = self.result

        query_model = QueryCriterionService(self.sqlModel, query_criteria)

        result = self.filter_list(query_model, result)
        result = self.search_list(query_model, result)
        result = self.sort_list(query_model, result)
        result = self.sort_by_pk(result)

        total_count = len(result.all())

        if length:
            result = result.limit(length)

        if start:
            result = result.offset(start)

        result = result.all()

        data_response_list = [self.response_schema.model_validate(el) for el in result]

        return data_response_list, total_count

    def get_record(self, id: int) -> K:
        result = self.session.query(self.sqlModel).get(id)

        if not result or result.deleted_at != None or not self.response_schema:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        data_response = self.response_schema.model_validate(result)

        return data_response

    def create_record(self, data: W) -> None:
        new_record = self.sqlModel(**data.model_dump())
        if self.current_user:
            new_record.created_by = self.current_user.user_id
        self.session.add(new_record)
        self.session.commit()
        return

    def update_record(self, data: W, id: int | None) -> None:
        result = self.session.query(self.sqlModel).get(id)

        if not result or result.deleted_at != None:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        model_to_dict = data.model_dump()

        for key, value in model_to_dict.items():
            setattr(result, key, value)

        if self.current_user:
            result.updated_by = self.current_user.user_id

        result.updated_at = func.now()
        self.session.commit()
        return

    def toggle_active(self, data: ActiveToggleDTO, id: int) -> None:
        result = self.session.query(self.sqlModel).get(id)

        if not result or result.deleted_at != None:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        result.is_active = data.is_active
        if self.current_user:
            result.updated_by = self.current_user.user_id
        result.updated_at = func.now()

        self.session.commit()
        return

    def delete_multiple(self, ids: list[int]) -> None:
        for id in ids:
            result = self.session.query(self.sqlModel).get(id)

            if result and result.deleted_at == None:
                result.deleted_at = func.now()
                if self.current_user:
                    result.deleted_by = self.current_user.user_id

        self.session.commit()
        return

    def delete_record(self, id: int) -> None:
        result = self.session.query(self.sqlModel).get(id)

        if not result or result.deleted_at != None:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        result.deleted_at = func.now()
        if self.current_user:
            result.deleted_by = self.current_user.user_id

        self.session.commit()
        return

    def filter_list(self, query_model: QueryCriterionService, result: Query) -> Query:
        result = result.filter(self.sqlModel.deleted_at == None)
        return query_model.filters(result, self.property_model_list)

    def search_list(self, query_model: QueryCriterionService, result: Query) -> Query:
        return query_model.search(result, self.property_search)

    def sort_list(self, query_model: QueryCriterionService, result: Query) -> Query:
        return query_model.sorts(result, self.property_model_list)

    def sort_by_pk(self, result: Query) -> Query:
        return result.order_by(self.default_sort)

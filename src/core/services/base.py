from datetime import datetime, timezone
from typing import Generic, Type, TypeVar

from fastapi import status
from sqlmodel import select

from core.classes.handle_exception import HandleException
from core.constants.generic_errors import GEN_4000
from core.database.database import SessionDep
from core.models.base import BaseAuditModel
from core.models.camel import CamelModel
from core.models.query import PropertyModel, QueryCriteria
from core.models.toggle import ActiveToggleDTO
from core.models.user import UserModel
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
        self.statement = select(self.sqlModel)
        self.default_sort = self.sqlModel.get_primary_key_name()
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

        statement = self.statement

        query_model = QueryCriterionService(self.sqlModel, query_criteria)

        statement = self.filter_list(query_model, statement)
        statement = self.search_list(query_model, statement)
        statement = self.sort_list(query_model, statement)
        statement = self.sort_by_pk(statement)

        total_count = len(self.session.exec(statement).all())

        if length:
            statement = statement.limit(length)

        if start:
            statement = statement.offset(start)

        result = self.session.exec(statement).all()

        data_response_list = [self.response_schema.model_validate(el) for el in result]

        return data_response_list, total_count

    def get_record(self, id: int) -> K:
        result = self.session.get(self.sqlModel, id)

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
        result = self.session.get(self.sqlModel, id)

        if not result or result.deleted_at != None:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        model_to_dict = data.model_dump()

        for key, value in model_to_dict.items():
            setattr(result, key, value)

        if self.current_user:
            result.updated_by = self.current_user.user_id

        result.updated_at = datetime.now(timezone.utc)
        self.session.commit()
        return

    def toggle_active(self, data: ActiveToggleDTO, id: int) -> None:
        result = self.session.get(self.sqlModel, id)

        if not result or result.deleted_at != None:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        result.is_active = data.is_active
        if self.current_user:
            result.updated_by = self.current_user.user_id
        result.updated_at = datetime.now(timezone.utc)

        self.session.commit()
        return

    def delete_multiple(self, ids: list[int]) -> None:
        for id in ids:
            result = self.session.get(self.sqlModel, id)

            if result and result.deleted_at == None:
                result.deleted_at = datetime.now(timezone.utc)
                if self.current_user:
                    result.deleted_by = self.current_user.user_id

        self.session.commit()
        return

    def delete_record(self, id: int) -> None:
        result = self.session.get(self.sqlModel, id)

        if not result or result.deleted_at != None:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        result.deleted_at = datetime.now(timezone.utc)
        if self.current_user:
            result.deleted_by = self.current_user.user_id

        self.session.commit()
        return

    def filter_list(self, query_model: QueryCriterionService, statement):
        result = statement.where(self.sqlModel.deleted_at == None)
        return query_model.filters(result, self.property_model_list)

    def search_list(self, query_model: QueryCriterionService, statement):
        return query_model.search(statement, self.property_search)

    def sort_list(self, query_model: QueryCriterionService, statement):
        return query_model.sorts(statement, self.property_model_list)

    def sort_by_pk(self, statement):
        return statement.order_by(self.default_sort)

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Generic, Type, TypeVar

from fastapi import status
from sqlmodel import select
from sqlmodel.sql.expression import SelectOfScalar

from src.core.classes.handle_exception import HandleException
from src.core.constants.generic_errors import GEN_4000
from src.core.database.database import SessionDep
from src.core.models.base import BaseAudit
from src.core.models.camel import Camel
from src.core.models.query import PropertyModel, QueryCriteria
from src.core.models.toggle import ActiveToggleDTO
from src.core.models.user import UserModel
from src.core.services.query import QueryCriterionService

T = TypeVar("T", bound=BaseAudit)
K = TypeVar("K", bound=Camel)
W = TypeVar("W", bound=Camel)


@dataclass
class BaseService(Generic[T, K, W]):
    session: SessionDep
    current_user: UserModel | None
    sql_model: Type[T]
    response_schema: Type[K]
    query_model = QueryCriterionService[T]()

    def get_records(
        self,
        start: int | None,
        length: int | None,
        query_criteria: QueryCriteria | None,
    ) -> tuple[list[K], int]:
        if not self.response_schema:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        statement = self.query_model.validate_query(
            query_criteria,
            self.get_statement(),
            self.get_property_model_list(),
            self.sql_model,
            self.get_property_search(),
        )

        total_count = len(self.session.exec(statement).all())

        if length:
            statement = statement.limit(length)

        if start:
            statement = statement.offset(start)

        result = self.session.exec(statement).all()

        data_response_list = [self.response_schema.model_validate(el) for el in result]

        return data_response_list, total_count

    def get_record(self, id: int) -> K:
        result = self.session.get(self.sql_model, id)

        if not result or result.deleted_at != None or not self.response_schema:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        data_response = self.response_schema.model_validate(result)

        return data_response

    def create_record(self, data: W) -> None:
        new_record = self.sql_model(**data.model_dump())
        if self.current_user:
            new_record.created_by = self.current_user.user_id
        self.session.add(new_record)
        self.session.commit()
        return

    def update_record(self, data: W, id: int | None) -> None:
        result = self.session.get(self.sql_model, id)

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
        result = self.session.get(self.sql_model, id)

        if not result or result.deleted_at != None:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        result.is_active = data.is_active
        if self.current_user:
            result.updated_by = self.current_user.user_id
        result.updated_at = datetime.now(timezone.utc)

        self.session.commit()
        return

    def delete_record(self, id: int) -> None:
        result = self.session.get(self.sql_model, id)

        if not result or result.deleted_at != None:
            raise HandleException([GEN_4000], status.HTTP_404_NOT_FOUND)

        result.deleted_at = datetime.now(timezone.utc)
        if self.current_user:
            result.deleted_by = self.current_user.user_id

        self.session.commit()
        return

    def get_statement(self) -> SelectOfScalar[T]:
        """Get base statement with optimized loading"""
        statement = select(self.sql_model).where(self.sql_model.deleted_at == None)

        # Apply custom statement modifications if available
        if hasattr(self, "get_optimized_statement"):
            return self.get_optimized_statement(statement)

        return statement

    def get_optimized_statement(
        self, base_statement: SelectOfScalar[T]
    ) -> SelectOfScalar[T]:
        """Get optimized statement with joins. Must be implemented by each service"""
        return base_statement

    def get_default_sort(self) -> str | None:
        return self.sql_model.get_primary_key_name()

    def get_property_model_list(self) -> list[PropertyModel]:
        return []

    def get_property_search(self) -> list:
        return (
            [getattr(self.sql_model, "name")] if hasattr(self.sql_model, "name") else []
        )

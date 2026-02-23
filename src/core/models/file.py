import sqlalchemy as sa
from pydantic.json_schema import SkipJsonSchema
from sqlmodel import BigInteger, Field

from src.core.models.base import BaseAudit
from src.core.models.camel import Camel


class FileBase(Camel):
    file_id: int | None = Field(sa_type=BigInteger, default=None, primary_key=True)
    source_file_name: str = Field(sa_column=sa.Column(sa.String, nullable=False))
    cdn_file_name: str = Field(sa_column=sa.Column(sa.String, nullable=False))
    mime_type: str | None = Field(sa_column=sa.Column(sa.String, nullable=False))
    file_size: int | None = Field(sa_column=sa.Column(sa.Integer, nullable=False))
    url: str = Field(sa_column=sa.Column(sa.String, nullable=False))


class File(FileBase, BaseAudit, table=True):
    __tablename__: str = "files"
    pass


class FileResponseDTO(FileBase):
    pass


class FileDTO(FileBase):
    file_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)

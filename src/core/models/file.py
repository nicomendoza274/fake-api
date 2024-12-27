from pydantic.json_schema import SkipJsonSchema
from sqlmodel import BigInteger, Field

from core.models.base import BaseAudit
from core.models.camel import Camel


class FileBase(Camel):
    source_file_name: str = Field()
    cdn_file_name: str = Field()
    mime_type: str | None = Field(nullable=True)
    file_size: int | None = Field(nullable=True)
    url: str = Field()


class File(FileBase, BaseAudit, table=True):
    __tablename__ = "files"  # type: ignore
    file_id: int | None = Field(sa_type=BigInteger, primary_key=True)


class FileResponseDTO(FileBase):
    file_id: int


class FileDTO(FileBase):
    file_id: SkipJsonSchema[int | None] = Field(default=None, exclude=True)

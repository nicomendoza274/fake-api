from sqlmodel import BigInteger, Field

from core.models.base import BaseAuditModel
from core.models.camel import CamelModel


class FileBase(CamelModel):
    file_id: int | None
    source_file_name: str
    cdn_file_name: str
    mime_type: str
    file_size: int
    url: str

    class Config:
        from_attributes = True


class FileResponseDTO(FileBase):
    pass


class FileDTO(FileBase):
    file_id: int | None = None


class FileModel(BaseAuditModel, table=True):
    __tablename__ = "files"  # type: ignore
    file_id: int | None = Field(sa_type=BigInteger, primary_key=True)
    source_file_name: str = Field()
    cdn_file_name: str = Field()
    mime_type: str | None = Field(nullable=True)
    file_size: int | None = Field(nullable=True)
    url: str = Field()

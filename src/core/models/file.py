from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from core.models.audit_model import AuditModel
from core.models.base import Base


class FileModel(Base, AuditModel):
    __tablename__ = "files"

    file_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    source_file_name: Mapped[str]
    cdn_file_name: Mapped[str]
    mime_type: Mapped[str]
    file_size: Mapped[int]
    url: Mapped[str]

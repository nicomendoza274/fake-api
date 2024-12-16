import shutil
import uuid
from typing import Type, TypeVar

from fastapi import Request, UploadFile
from sqlalchemy import func
from sqlalchemy.orm.session import Session

from core.constants.file import UPLOAD_DIRECTORY
from core.models.base import Base
from core.models.file import FileModel
from core.models.user import UserModel

T = TypeVar("T", bound=Base)


class FileService:
    def __init__(self, db: Session, user: UserModel | None) -> None:
        self.db = db
        self.user = user

    def save_file(self, file: UploadFile | None, request: Request) -> FileModel | None:
        if not file or not file.filename:
            return None

        file_extension = file.filename.split(".")[-1]
        new_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = f"{UPLOAD_DIRECTORY}/{new_filename}"
        base_url = request.base_url

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        new_file = FileModel(
            source_file_name=file.filename,
            cdn_file_name=new_filename,
            mime_type=file.content_type,
            file_size=file.size,
            url=f"{base_url}api/{UPLOAD_DIRECTORY}/{new_filename}",
            created_by=self.user.user_id if self.user else None,
        )

        self.db.add(new_file)
        self.db.flush()
        self.db.refresh(new_file)

        return new_file

    def delete_file(self, model: Type[T], id: int | None, file_id_name: str) -> None:
        result = self.db.query(model).get(id)

        file_id = getattr(result, file_id_name)
        if not result or result.deleted_at or not file_id:
            return None

        file = self.db.query(FileModel).get(file_id)

        if not file or file.deleted_at:
            return None

        file.deleted_at = func.now()
        if self.user:
            file.deleted_by = self.user.user_id

        self.db.flush()
        self.db.refresh(file)

        return None

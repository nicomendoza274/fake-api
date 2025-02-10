import shutil
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Type, TypeVar

from fastapi import Request, UploadFile

from core.constants.file import UPLOAD_DIRECTORY
from core.database.database import SessionDep
from core.models.base import BaseAudit
from core.models.file import File
from core.models.user import UserModel

T = TypeVar("T", bound=BaseAudit)


@dataclass
class FileService:
    session: SessionDep
    user: UserModel | None

    def save_file(self, file: UploadFile | None, request: Request) -> File | None:
        if not file or not file.filename:
            return None

        file_extension = file.filename.split(".")[-1]
        new_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = f"{UPLOAD_DIRECTORY}/{new_filename}"
        base_url = request.base_url

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        new_file = File(
            file_id=None,
            source_file_name=file.filename,
            cdn_file_name=new_filename,
            mime_type=file.content_type,
            file_size=file.size,
            url=f"{base_url}api/{UPLOAD_DIRECTORY}/{new_filename}",
            created_by=self.user.user_id if self.user else None,
        )

        self.session.add(new_file)
        self.session.flush()
        self.session.refresh(new_file)

        return new_file

    def delete_file(self, model: Type[T], id: int | None, file_id_name: str) -> None:
        result = self.session.get(model, id)

        file_id = getattr(result, file_id_name)
        if not result or result.deleted_at or not file_id:
            return None

        file = self.session.get(File, id)

        if not file or file.deleted_at:
            return None

        file.deleted_at = datetime.now(timezone.utc)
        if self.user:
            file.deleted_by = self.user.user_id

        self.session.flush()
        self.session.refresh(file)

        return None

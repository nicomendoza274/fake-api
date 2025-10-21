import os

from fastapi import HTTPException, UploadFile, status

from core.classes.settings import settings


class FileValidationError(Exception):
    """Custom exception for file validation errors"""

    pass


def validate_file_size(file: UploadFile) -> None:
    """Validate file size"""
    if not file:
        return

    max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024

    # Read file to get real size
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB",
        )


def validate_file_type(file: UploadFile) -> None:
    """Validar el tipo MIME del archivo"""
    if not file or not file.content_type:
        return

    allowed_types = settings.ALLOWED_FILE_TYPES.split(",")

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type '{file.content_type}' is not allowed. Allowed types: {', '.join(allowed_types)}",
        )


def validate_file_extension(file: UploadFile) -> None:
    """Validar la extensión del archivo"""
    if not file or not file.filename:
        return

    # MIME types to allowed extensions mapping
    mime_to_extensions = {
        "image/jpeg": [".jpg", ".jpeg"],
        "image/png": [".png"],
        "image/gif": [".gif"],
        "application/pdf": [".pdf"],
    }

    allowed_types = settings.ALLOWED_FILE_TYPES

    for mime_type in allowed_types:
        if file.content_type == mime_type:
            allowed_extensions = mime_to_extensions.get(mime_type, [])
            if allowed_extensions:
                file_extension = os.path.splitext(file.filename.lower())[1]
                if file_extension not in allowed_extensions:
                    raise HTTPException(
                        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                        detail=f"File extension '{file_extension}' does not match content type '{mime_type}'",
                    )


def validate_file_security(file: UploadFile) -> None:
    """Validar la seguridad del archivo (verificar que no sea ejecutable)"""
    if not file or not file.filename:
        return

    # Dangerous extensions list
    dangerous_extensions = [
        ".exe",
        ".bat",
        ".cmd",
        ".com",
        ".pif",
        ".scr",
        ".vbs",
        ".js",
        ".jar",
        ".php",
        ".asp",
        ".aspx",
        ".jsp",
        ".sh",
        ".ps1",
        ".py",
        ".pl",
        ".rb",
    ]

    file_extension = os.path.splitext(file.filename.lower())[1]

    if file_extension in dangerous_extensions:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File extension '{file_extension}' is not allowed for security reasons",
        )


def validate_upload_file(file: UploadFile) -> None:
    """Validación completa del archivo de upload"""
    if not file:
        return

    # Validate size
    validate_file_size(file)

    # Validate MIME type
    validate_file_type(file)

    # Validate extension
    validate_file_extension(file)

    # Validate security
    validate_file_security(file)

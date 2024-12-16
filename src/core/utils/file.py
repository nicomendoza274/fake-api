import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.constants.file import UPLOAD_DIRECTORY


def create_and_mount_static_directory(app: FastAPI) -> None:
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
    app.mount(
        f"/api/{UPLOAD_DIRECTORY}",
        StaticFiles(directory=UPLOAD_DIRECTORY),
        name=UPLOAD_DIRECTORY,
    )

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from core.middlewares.error_handler import ErrorHandler
from core.utils.file import create_and_mount_static_directory
from routers.auth import auth
from routers.category import category
from routers.customer import customer
from routers.product import product
from routers.role import role
from routers.user import user

app = FastAPI()

create_and_mount_static_directory(app)

app.title = "Fake API"
app.description = "This is a template API"
app.version = "2.1.0"

app_prefix = "/api"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ErrorHandler)
app.include_router(auth, prefix=app_prefix)
app.include_router(category, prefix=app_prefix)
app.include_router(customer, prefix=app_prefix)
app.include_router(product, prefix=app_prefix)
app.include_router(role, prefix=app_prefix)
app.include_router(user, prefix=app_prefix)


@app.get("/", include_in_schema=False)
def main():
    return RedirectResponse(url="/docs/")

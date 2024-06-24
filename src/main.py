from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from core.middlewares.error_handler import ErrorHandler
from routers.auth import auth_router
from routers.category import category_router
from routers.customer import customer_router
from routers.product import product_router
from routers.role import role_router
from routers.user import user_router

app = FastAPI()


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
app.include_router(auth_router, prefix=app_prefix)
app.include_router(user_router, prefix=app_prefix)
app.include_router(role_router, prefix=app_prefix)
app.include_router(customer_router, prefix=app_prefix)
app.include_router(category_router, prefix=app_prefix)
app.include_router(product_router, prefix=app_prefix)


@app.get("/", include_in_schema=False)
def main():
    return RedirectResponse(url="/docs/")

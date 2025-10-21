from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from core.classes.settings import settings
from core.middlewares.error_handler import ErrorHandler
from core.middlewares.rate_limiter import RateLimitMiddleware
from core.utils.file import create_and_mount_static_directory
from routers import auth, category, customer, health, product, role, user

app = FastAPI()

create_and_mount_static_directory(app)

app.title = "Fake API"
app.description = "This is a template API"
app.version = "2.1.0"

app_prefix = "/api"

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(ErrorHandler)

app.include_router(auth.router, prefix=app_prefix)
app.include_router(category.router, prefix=app_prefix)
app.include_router(customer.router, prefix=app_prefix)
app.include_router(product.router, prefix=app_prefix)
app.include_router(role.router, prefix=app_prefix)
app.include_router(user.router, prefix=app_prefix)
app.include_router(health.router, prefix=app_prefix)


@app.get("/", include_in_schema=False)
def main():
    return RedirectResponse(url="/docs/")

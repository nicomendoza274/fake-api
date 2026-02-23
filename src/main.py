from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from src.core.classes.settings import settings
from src.core.middlewares.error_handler import ErrorHandler
from src.core.middlewares.rate_limiter import RateLimitMiddleware
from src.core.utils.file import create_and_mount_static_directory
from src.routers import auth, category, customer, health, product, role, user

app = FastAPI(
    title="Fake API",
    description="This is a template API",
    version="2.1.0",
)

create_and_mount_static_directory(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(ErrorHandler)

app.include_router(auth.router, prefix="/api")
app.include_router(category.router, prefix="/api")
app.include_router(customer.router, prefix="/api")
app.include_router(product.router, prefix="/api")
app.include_router(role.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(health.router, prefix="/api")


@app.get("/", include_in_schema=False)
def main():
    return RedirectResponse(url="/docs/")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from config.database import Base, engine
from middlewares.error_handler import ErrorHandler
from routers.category import category_router
from routers.customer import customer_router
from routers.product import product_router
from routers.role import role_router
from routers.user import user_router
from routers.user_role import user_role_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
]

app.title = "Fake API"
app.description = "This is an imitation API designed to connect with a Frontend"
app.version = "1.4.0"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(ErrorHandler)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(user_role_router)
app.include_router(customer_router)
app.include_router(category_router)
app.include_router(product_router)


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

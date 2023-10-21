from fastapi import FastAPI
from starlette.responses import RedirectResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.user import user_router
from routers.customer import customer_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.title = "Fake API"
app.version = "1.0.0"

app.add_middleware(ErrorHandler)
app.include_router(user_router)
app.include_router(customer_router)


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

from humps import camelize
from sqlmodel import SQLModel


class CamelModel(SQLModel):
    class Config:
        alias_generator = camelize
        populate_by_name = True

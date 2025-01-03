from humps import camelize
from sqlmodel import SQLModel


class Camel(SQLModel):
    class Config:
        alias_generator = camelize
        populate_by_name = True

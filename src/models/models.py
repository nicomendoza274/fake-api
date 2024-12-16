from sqlalchemy import BigInteger, ForeignKey, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import BaseAuditModel
from core.models.file import FileModel
from core.models.user import UserModel


class UserCode(BaseAuditModel):
    __tablename__ = "user_codes"

    user_code_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=True)


class UserRole(BaseAuditModel):
    __tablename__ = "user_roles"

    user_role_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    role_id: Mapped[int | None] = mapped_column(
        ForeignKey("roles.role_id"), nullable=True
    )


class User(UserModel, BaseAuditModel):
    __tablename__ = "users"

    picture_id: Mapped[int | None] = mapped_column(
        ForeignKey("files.file_id"), nullable=True
    )

    picture: Mapped[FileModel] = relationship(
        primaryjoin=and_(
            FileModel.file_id == picture_id,
            FileModel.deleted_at == None,
        )
    )


class Role(BaseAuditModel):
    __tablename__ = "roles"

    role_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]


class Category(BaseAuditModel):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Customer(BaseAuditModel):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    internal_id: Mapped[str]
    address: Mapped[str]
    city: Mapped[str]
    phone: Mapped[str]


class Product(BaseAuditModel):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]
    is_active: Mapped[bool]

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.category_id"), nullable=True
    )

    picture_id: Mapped[int | None] = mapped_column(
        ForeignKey("files.file_id"), nullable=True
    )

    picture: Mapped[FileModel] = relationship(
        primaryjoin=and_(
            FileModel.file_id == picture_id,
            FileModel.deleted_at == None,
        )
    )

    category: Mapped["Category"] = relationship(
        primaryjoin=and_(
            Category.category_id == category_id,
            Category.deleted_at == None,
        )
    )

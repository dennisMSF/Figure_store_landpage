from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlmodel import Field, SQLModel


class Company(SQLModel, table=True):   # table=True: esta clase es una tabla
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

class Figure(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint("stock >= 0", name="ck_stock_quantity"),
        CheckConstraint("price >= 0", name="ck_price_value"),
        UniqueConstraint("name", "series_id", name="uq_product_name_series"),
    )
    id: int | None = Field(default=None, primary_key=True)
    name: str
    height_cn: int | None = None
    price: int
    stock: int = 0
    code_jan: str
    company_id: int = Field(foreign_key="company.id", ondelete="RESTRICT")
    character_id: int = Field(foreign_key="character.id", ondelete="RESTRICT")
    scale: str | None = None
    photos_id: int = Field(foreign_key="photos.id", ondelete="CASCADE")
    type_id: int = Field(foreign_key="type.id", ondelete="RESTRICT")
    published: int = 0
    description: str | None = None

class Character(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    series_id: int = Field(foreign_key="series.id", ondelete="RESTRICT")

class Series(SQLModel, table=True):
    id: int | None = Field(deafult=None, primary_key=True)
    nombre: str = Field(unique=True)
    
class Photos(SQLModel, table=True):
    id: int | None = Field(deafult=None, primary_key=True)
    directory: str


class Type(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)

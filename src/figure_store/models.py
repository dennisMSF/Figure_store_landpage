from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlmodel import Field, SQLModel


class Manufacturer(SQLModel, table=True):   # table=True: esta clase es una tabla
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

class Figure(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint("stock >= 0", name="ck_stock_quantity"),
        CheckConstraint("price > 0", name="ck_price_value")   
    )
    id: int | None = Field(default=None, primary_key=True)
    name: str
    height_mm: int | None = None
    price: int
    stock: int = 0
    code_jan: str = Field(unique=True)
    company_id: int = Field(foreign_key="manufacturer.id", ondelete="RESTRICT")
    character_id: int = Field(foreign_key="character.id", ondelete="RESTRICT")
    scale: str | None = None
    type_id: int = Field(foreign_key="type.id", ondelete="RESTRICT")
    published: bool = 0
    description: str | None = None

class Character(SQLModel, table=True):
    __table_args__ = (
            UniqueConstraint("name","series_id", name="uq_figure_name_series"),
    )
    id: int | None = Field(default=None, primary_key=True)
    name: str
    series_id: int = Field(foreign_key="series.id", ondelete="RESTRICT")

class Series(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    
class Photos(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    photo_path: str
    orden: int
    texto_alt: str
    figure_id: int = Field(foreign_key="figure.id", ondelete="CASCADE")


class Type(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)

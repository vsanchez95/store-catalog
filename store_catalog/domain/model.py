"""Domain model module.

This module define the Entities, Value Objects and Domain servies of the Domain Model.
"""

from __future__ import annotations

from typing_extensions import Annotated

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import HttpUrl
from pydantic import StringConstraints


class ProductManufacturer(BaseModel):
    """Product manufacturer domain model class.

    Attributes:
        id_ (str): manufacturer ID.
        title (str): title of manufacturer (unique).
        image (HttpUrl): image URL of manufacturer.
    """

    model_config = ConfigDict(populate_by_name=True)

    id_: Annotated[int, Field(alias='id')]
    title: Annotated[str, StringConstraints(min_length=1)]
    image: HttpUrl


class ProductCategory(BaseModel):
    """Product category domain model calss.

    Attributes:
        id_ (str): category ID.
        title (str): title of category (unique).
        subcategory (bool): True if category is a subcategory else False.
        category_parent (ProductCategory, optional): category parent if category is a subcategory.
    """

    model_config = ConfigDict(populate_by_name=True)

    id_: Annotated[int, Field(alias='id')]
    title: Annotated[str, StringConstraints(min_length=1)]
    subcategory: bool = False
    category_parent: ProductCategory | None = None


class ProductModel(BaseModel):
    """Model domain model class.

    Attributes:
        sku (str): stock-keeping unit. It is a unique identifier.
        title (str): product title.
        description (str): product model description.
        image (HttpUrl): product model image URL.
        category (ProductCategory): product model category (it is always a subcategory).
        manufacturer (ProductManufacturer): product model manufacturer.
        min_price (float): min product model price in euros.
    """

    sku: Annotated[str, StringConstraints(min_length=1)]
    title: Annotated[str, StringConstraints(min_length=1)]
    description: Annotated[str, StringConstraints(min_length=1)]
    image: HttpUrl
    category: ProductCategory
    manufacturer: ProductManufacturer
    min_price: float


class Product(BaseModel):
    """Product domain model class.

    Attributes:
        sku (str): stock-keeping unit. It is a unique identifier.
        title (str): product title.
        description (str): product description.
        image (HttpUrl): product image URL.
        price (float): product price in euros.
        model (Model): product model.
        stock (bool): True if product in stock else False.
        num_purchases (int): numbrer of purchases of a product.
    """
    sku: Annotated[str, StringConstraints(min_length=1)]
    title: Annotated[str, StringConstraints(min_length=1)]
    description: Annotated[str, StringConstraints(min_length=1)]
    image: HttpUrl
    price: float
    model: ProductModel
    stock: bool
    num_purchases: int

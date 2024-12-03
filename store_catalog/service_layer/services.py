"""Service Layern module.

This module define a layer of services.
"""
from typing import Any

from store_catalog.adapters.repository import AbstractProductRepository
from store_catalog.domain.model import Product


class ProductSearcher:
    """Product searcher service.

    Attributes:
        _repository [AbstractProductRepository]: repository to search products.

    """
    def __init__(self, repository: AbstractProductRepository):
        self._repository = repository

    def __call__(self, sku: str | None = None, *args: Any, **kwargs: Any) -> Product | None | list[Product]:
        if sku is not None:
            return self._repository.get(sku=sku)

        return self._repository.list(*args, **kwargs)

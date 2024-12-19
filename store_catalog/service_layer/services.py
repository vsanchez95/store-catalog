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
        """Constructor.

        Args:
            repository (AbstractProductRepository): repository to search products.

        """
        self._repository = repository

    def __call__(self, sku: str | None = None, *args: Any, **kwargs: Any) -> Product | None | list[Product]:
        """Search products.

        Args:
            sku (str, optional): stock-keeping unit.
            *args (Any): additional arguments.
            **kwargs (Any): additional key-word arguments.

        Returns:
            Product | None | list[Product]: product, list of products or None.

        """
        if sku is not None:
            return self._repository.get(sku=sku)

        return self._repository.list(*args, **kwargs)

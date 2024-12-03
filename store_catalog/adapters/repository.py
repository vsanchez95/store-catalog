"""Repository module.

This module define a layer of abstraction around search engine access.
"""

from abc import ABC
from abc import abstractmethod
from contextlib import AbstractContextManager
from typing import Any
from typing import Callable

from typesense import Client as TypesenseClient  # type: ignore

from store_catalog.domain.model import Product
from store_catalog.domain.model import ProductCategory
from store_catalog.domain.model import ProductManufacturer
from store_catalog.domain.model import ProductModel


class ProductNotFoundError(Exception):
    ...


class ProductMultipleFoundsError(Exception):
    ...


class AbstractProductRepository(ABC):
    """Abstract product repository class Port (interface).
    """

    @abstractmethod
    def get(self, sku: str) -> Product | None:
        raise NotImplementedError

    @abstractmethod
    def list(self, *args: Any, **kwargs: Any) -> list[Product]:
        raise NotImplementedError


class TypesenseProductRepository(AbstractProductRepository):
    """Typesense product repository class Adapter.

    Attributes:
        _session_factory (Callable[..., AbstractContextManager[TypesenseClient]]): typesense client session factory.

    """
    COLLECTION_NAME: str = 'products'
    INCLUDE_FIELDS: str = ('$product_models(*, $product_categories(*, $product_categories(*)),'
                           '$product_manufacturers(*))')

    def __init__(self, session_factory: Callable[..., AbstractContextManager[TypesenseClient]]) -> None:
        self._session_factory: Callable[..., AbstractContextManager[TypesenseClient]] = session_factory

    @staticmethod
    def _product_document_to_product(product_document: dict) -> Product:
        """Mapper a product document of typesense products collection to a Product domain model.
        Args:
            product_document (dict): product document of products collection of typesense.

        Returns:
            Product: product domain model.

        """
        return Product(
            sku=product_document['sku'],
            title=product_document['title'],
            description=product_document['description'],
            image=product_document['image_url'],
            price=product_document['price'],
            model=ProductModel(
                sku=product_document['product_models']['sku'],
                title=product_document['product_models']['title'],
                description=product_document['product_models']['description'],
                image=product_document['product_models']['image_url'],
                min_price=product_document['product_models']['min_price'],
                category=ProductCategory(
                    id_=product_document['product_models']['product_categories']['id'],
                    title=product_document['product_models']['product_categories']['title'],
                    subcategory=product_document['product_models']['product_categories']['subcategory'],
                    category_parent=ProductCategory(
                        id_=product_document
                        ['product_models']
                        ['product_categories']
                        ['product_categories']
                        ['id'],
                        title=product_document
                        ['product_models']
                        ['product_categories']
                        ['product_categories']
                        ['title'],
                    )
                ),
                manufacturer=ProductManufacturer(
                    id_=product_document['product_models']['product_manufacturers']['id'],
                    title=product_document['product_models']['product_manufacturers']['title'],
                    image=product_document['product_models']['product_manufacturers']['image_url'],
                ),
            ),
            stock=product_document['stock'],
            num_purchases=0,
        )

    def get(self, sku: str) -> Product | None:
        """Get product with sku from Typesense products collection.

        Args:
            sku (str): SKU of product to get.

        Returns:
            Product | None: Product found if exists else None.

        Raises:
            ProductNotFoundError: if product with sku not exists
            ProductMultipleFoundsError: if several products with that sku.

        """
        with self._session_factory() as session:
            products_hits: list[dict] = session.collections[self.COLLECTION_NAME].documents.search(dict(
                q=sku,
                query_by='sku',
                include_fields=self.INCLUDE_FIELDS,
            ))['hits']

            if len(products_hits) == 0:
                raise ProductNotFoundError
            elif len(products_hits) > 1:
                raise ProductMultipleFoundsError

            return self._product_document_to_product(product_document=products_hits[0]['document'])

    def list(self, *args: Any, **kwargs: Any) -> list[Product]:
        """Search in Typesense products collection and return products found list.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitary kwyword arguments with search parameters.

        Returns:
            list[Product]: list of Products found in products Typesense collection.
        """
        with self._session_factory() as session:
            # TODO: improve search parameters adn options (https://typesense.org/docs/27.1/api/search.html)
            products_hits: list[dict] = session.collections['products'].documents.search({
                **kwargs,
                'include_fields': self.INCLUDE_FIELDS,
            })['hits']

            products_documents: list[dict] = [field['document'] for field in products_hits]

            return [self._product_document_to_product(product_document) for product_document in products_documents]

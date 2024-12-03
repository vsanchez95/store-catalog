"""Container Dependency Injector module.

This module define container of Dependency Injector use to explicit dependencies.
"""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration
from dependency_injector.providers import Factory
from dependency_injector.providers import Singleton

from store_catalog.adapters.repository import TypesenseProductRepository
from store_catalog.adapters.typesense_database import TypesenseDatabase
from store_catalog.service_layer.services import ProductSearcher


class Container(DeclarativeContainer):
    """Container dependency injector.

    """
    config: Configuration = Configuration()
    typesense_database: Singleton = Singleton(
        TypesenseDatabase,
        api_key=config.TYPESENSE_API_KEY,
        host=config.TYPESENSE_HOST,
        port=config.TYPESENSE_PORT,
        protocol=config.TYPESENSE_PROTOCOL,
    )

    product_repository: Factory = Factory(
        TypesenseProductRepository,
        session_factory=typesense_database.provided.session,
    )
    product_searcher: Singleton = Singleton(ProductSearcher, repository=product_repository)

import os
from json import loads as json_loads

from djangoproject.django_project.settings import TYPESENSE_API_KEY
from djangoproject.django_project.settings import TYPESENSE_HOST
from djangoproject.django_project.settings import TYPESENSE_PORT
from djangoproject.django_project.settings import TYPESENSE_PROTOCOL
from store_catalog.adapters.typesense_database import TypesenseDatabase
from store_catalog.container import Container

CATALOG_DIR_PATH: str = os.getenv('CATALOG_DIR_PATH', '.')

container: Container = Container()

typense_database: TypesenseDatabase = container.typesense_database(
    api_key=TYPESENSE_API_KEY,
    host=TYPESENSE_HOST,
    port=TYPESENSE_PORT,
    protocol=TYPESENSE_PROTOCOL,
)

with typense_database.session() as session:
    # Create collections
    # Product Manufacturers
    session.collections.create({
        'name': 'product_manufacturers',
        'fields': [
            {'name': 'title', 'type': 'string'},
            {'name': 'image_url', 'type': 'string', 'optional': True},
        ],
    })

    # Product Categories
    session.collections.create({
        'name': 'product_categories',
        'fields': [
            {'name': 'title', 'type': 'string'},
            {'name': 'subcategory', 'type': 'bool'},
            {
                'name': 'product_category_id',
                'type': 'string',
                'optional': True,
                'facet': True,
                'reference': 'product_categories.id',
            },
        ],
    })

    # Product Models
    session.collections.create({
        'name': 'product_models',
        'fields': [
            {'name': 'sku', 'type': 'string'},
            {'name': 'title', 'type': 'string'},
            {'name': 'description', 'type': 'string'},
            {'name': 'image_url', 'type': 'string'},
            {
                'name': 'product_category_id',
                'type': 'string',
                'facet': True,
                'reference': 'product_categories.id',
            },
            {
                'name': 'product_manufacturer_id',
                'type': 'string',
                'facet': True,
                'reference': 'product_manufacturers.id',
            },
            {'name': 'min_price', 'type': 'float'},
        ],
    })

    # Products
    session.collections.create({
        'name': 'products',
        'fields': [
            {'name': 'sku', 'type': 'string'},
            {'name': 'title', 'type': 'string'},
            {'name': 'description', 'type': 'string'},
            {'name': 'image_url', 'type': 'string'},
            {'name': 'price', 'type': 'float'},
            {
                'name': 'product_model_id',
                'type': 'string',
                'facet': True,
                'reference': 'product_models.id',
            },
            {'name': 'stock', 'type': 'bool'},
            {'name': 'num_reviews', 'type': 'int32'},
        ],
    })

    # Index documents
    product_manufacturers: list[dict] = []
    product_categories: list[dict] = []
    product_subcategories: list[dict] = []
    product_models: list[dict] = []
    products: list[dict] = []

    # Product Manufacturers
    with open(os.path.join(CATALOG_DIR_PATH, 'product_manufactures.jsonl')) as infile:
        for json_line in infile:
            product_manufacturers.append(json_loads(json_line))

    session.collections['product_manufacturers'].documents.import_(product_manufacturers)

    # Product Categories and Subcategories
    with open(os.path.join(CATALOG_DIR_PATH, 'product_categories.jsonl')) as infile:
        for json_line in infile:
            product_categories.append(json_loads(json_line))

    session.collections['product_categories'].documents.import_(product_categories)

    with open(os.path.join(CATALOG_DIR_PATH, 'product_subcategories.jsonl')) as infile:
        for json_line in infile:
            product_subcategories.append(json_loads(json_line))

    session.collections['product_categories'].documents.import_(product_subcategories)

    # Product Models
    with open(os.path.join(CATALOG_DIR_PATH, 'product_models.jsonl')) as infile:
        for json_line in infile:
            product_models.append(json_loads(json_line))

    session.collections['product_models'].documents.import_(product_models)

    # Products
    with open(os.path.join(CATALOG_DIR_PATH, 'products.jsonl')) as infile:
        for json_line in infile:
            products.append(json_loads(json_line))

    session.collections['products'].documents.import_(products)

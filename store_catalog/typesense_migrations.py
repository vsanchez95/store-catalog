from djangoproject.django_project import container
from store_catalog.adapters.typesense_database import TypesenseDatabase

typesense_database: TypesenseDatabase = container.typesense_database()


with typesense_database.session() as session:
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
            {'name': 'num_purchases', 'type': 'int32'},
        ],
    })

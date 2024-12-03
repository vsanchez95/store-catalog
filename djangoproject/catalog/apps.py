from django.apps import AppConfig

from djangoproject.django_project import container


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangoproject.catalog'

    def ready(self) -> None:
        container.wire(modules=['djangoproject.catalog.views'])

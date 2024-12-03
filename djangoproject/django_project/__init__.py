from djangoproject.django_project import settings
from store_catalog.container import Container

container = Container()
container.config.from_dict(settings.__dict__)

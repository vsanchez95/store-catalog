# Logiscenter - Catalog browser store

## Project structure

### [Domain modeling (DDD)](store_catalog/domain)
* #### [Domain model entities](store_catalog/domain)
* #### [Adapters infrastructure (Repository pattern)](store_catalog/adapters)
* #### [Services (Service Layer pattern)](store_catalog/service_layer)
### [Container of a Dependency Injector (Dependency Inversion Principle of SOLID)](store_catalog/container.py)
Dependency Injector is a dependency injection framework for Python: 
[Dependency Injector docs](https://python-dependency-injector.ets-labs.org/index.html).

Using this framework facilitates the principle of dependency inversion (SOLID).

It uses different design patterns (Factory, Singleton, Strategy, etc) which help develop 
code with high cohesion and low coupling.

Above all, it offers three major advantages:
* **Flexibility**. The components are loosely coupled. You can easily extend or change the functionality
of a system by combining the components in a different way. You even can do it on the fly.
* **Clearness and maintainability**. Dependency injection helps you reveal the dependencies.
Implicit becomes explicit. And “Explicit is better than implicit” (PEP 20 - The Zen of Python).
You have all the components and dependencies defined explicitly in a container.
This provides an overview and control of the application structure. It is easier to understand and change it.
* **Testability**. Testing is easier because you can easily inject mocks instead of real objects
that use API or database, etc.

### [Entrypoints](djangoproject/catalog/views.py)
djangoproject package, django project that serves as input to the system, with the list view of catalog products
where product searches can be performed.


## Typesense migrations and data index
* [Typesense schemas](store_catalog/typesense_migrations.py)
* [JSONL with catalog data to index](tests/catalog_files)

## Getting start
### Installation and activate viertualenv
```bash
poetry install --no-root --no-directory
poetry shell
```

### Linter PEP8 check
```bash
flake8 .
```

### Mypy check types
```bash
mypy .
```

### Pytest run tests
```bash
pytest -vvv
```

### Run local environment
```bash
make up
```

Check it: [Catalog navigator](http://localhost)


## Notes
Some packages used:
* Dependency management with [Poetry](https://python-poetry.org/docs/)
* Validating Domain Modeling with [Pydantic](https://docs.pydantic.dev/latest/)
* [Dependency injection for Python](https://python-dependency-injector.ets-labs.org/index.html)
* [Typesense API client for Python](https://github.com/typesense/typesense-python)
* Static type checker [mypy](https://mypy-lang.org/)
* Testing with [pytest](https://docs.pytest.org/en/stable/)

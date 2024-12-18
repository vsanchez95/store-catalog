# pull official base image
FROM python:3.12-slim

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /usr/src

# install system dependencies
RUN apt-get update && apt-get install -y netcat-traditional

# install python dependencies
RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false
COPY ./pyproject.toml .
RUN poetry install --no-root --no-directory

# copy project
COPY ./djangoproject djangoproject
COPY ./store_catalog store_catalog
COPY ./tests/wait_for_typesense.py .

CMD python wait_for_typesense.py && \
    python store_catalog/typesense_migrations.py && \
    python djangoproject/manage.py migrate && \
    python djangoproject/manage.py runserver 0.0.0.0:8000

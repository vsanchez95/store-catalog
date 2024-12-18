import time

from requests.exceptions import ConnectionError

from djangoproject.django_project import container
from store_catalog.adapters.typesense_database import TypesenseDatabase


typesense_database: TypesenseDatabase = container.typesense_database()


def wait_for_typesense_to_come_up() -> None:
    deadline: float = time.time() + 10
    typesense_ok: bool = False

    with typesense_database.session() as session:
        while time.time() < deadline:
            try:
                if not session.operations.is_healthy():
                    time.sleep(0.5)
                else:
                    typesense_ok = True
            except ConnectionError:
                time.sleep(0.5)

    if not typesense_ok:
        raise Exception('Typesense never came up')


if __name__ == '__main__':
    wait_for_typesense_to_come_up()

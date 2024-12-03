"""Typesense database client config module.
"""

from contextlib import contextmanager
from typing import Iterator

from typesense import Client as TypesenseClient  # type: ignore


class TypesenseDatabase(object):
    """Singleton to manage typesense client connections.

    """
    # TODO: improve with multiple nodes config
    def __init__(self, api_key: str, host: str, port: str, protocol: str) -> None:
        self._session_factory = lambda: TypesenseClient(config_dict=dict(
            api_key=api_key,
            nodes=[
                dict(host=host, port=port, protocol=protocol),
            ],
            connection_timeoud_seconds=10,
        ))

    @contextmanager
    def session(self) -> Iterator[TypesenseClient]:
        typesense_client: TypesenseClient = self._session_factory()
        yield typesense_client

"""Typesense database client config module.
"""

from collections.abc import Callable
from contextlib import contextmanager
from typing import Iterator

from typesense import Client as TypesenseClient  # type: ignore


class TypesenseDatabase(object):
    """Singleton to manage typesense client connections.

    Attributes:
        _session_factory (Callable): The factory to create a typesense client.

    """
    # TODO: improve with multiple nodes config
    def __init__(self, api_key: str, host: str, port: str, protocol: str) -> None:
        """Constructor.

        Args:
            api_key (str): The API key for the typesense client.
            host (str): The host of the typesense client.
            port (str): The port of the typesense client.
            protocol (str): The protocol of the typesense client.

        """
        self._session_factory: Callable[..., TypesenseClient] = lambda: TypesenseClient(config_dict=dict(
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

import os
import datetime
from typing import Union

from aiohttp import ClientSession
from aiohttp_client_cache import CachedSession, SQLiteBackend

from .exceptions import WrongDirectory


class Client:
    """A client for making async HTTP requests with optional caching.

    Args:
        session (Union[ClientSession, CachedSession]): The session to use for making requests.
        backend (Union[None, SQLiteBackend]): The backend to use for caching.
        enabled (bool): Whether caching is enabled or not.
    """

    def __init__(
        self,
        session: Union[None, ClientSession, CachedSession] = None,
        backend: Union[None, SQLiteBackend] = None,
        enabled: bool = False,
    ):
        self._session = session
        self._backend = backend
        self._enabled = enabled

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    @property
    def session(self):
        """The current session object.

        Returns:
            Union[ClientSession, CachedSession]: The current session object.
        """
        return self._session

    @session.setter
    def session(self, value):
        """Sets the session attribute of the class.

        Args:
            value: The value to set the session attribute to.

        Raises:
            AttributeError: If the user attempts to modify the immutable session attribute.
        """
        raise AttributeError("Can't modify immutable attribute session")

    @property
    def backend(self):
        """The current caching backend.

        Returns:
            Union[None, SQLiteBackend]: The current caching backend.
        """
        return self._backend

    @backend.setter
    def backend(self, value):
        """Sets the backend attribute of the class.

        Args:
            value: The value to set the backend attribute to.

        Raises:
            AttributeError: If the user attempts to modify the immutable backend attribute.
        """
        raise AttributeError("Can't modify immutable attribute backend")

    @property
    def enabled(self):
        """Whether caching is enabled or not.

        Returns:
            bool: Whether caching is enabled or not.
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        raise AttributeError("Can't modify immutable attribute enabled")

    @staticmethod
    def path_create(path: str) -> str:
        """Create a cache path.
        Args:
            path (str): Directory for a cache file.
        Returns:
            str: Concatenated path.
        Raises:
            WrongDirectory: The provider directory for a cache does not exist.
        """
        if not os.path.exists(path):
            raise WrongDirectory()
        return os.path.join(path, "pywarsaw_cache")

    async def cache_enable(
        self,
        path: str = os.getcwd(),
        expire_after: Union[
            None, int, float, str, datetime.datetime, datetime.timedelta
        ] = 3600,
        force_clear: bool = False,
        clear_expired: bool = False,
    ) -> None:
        """Enable caching using the SQLite backend.
        Args:
            path (str): Directory for the cache file. Defaults to current workind directory.
            expire_after (Union[None, int, float, str, datetime.datetime, datetime.timedelta]):
                Expiration time for the cache. Defaults to 3600.
            force_clear (bool): Clear the cache upon initialization. Defaults to False.
            clear_expired (bool): Clear expired cache upon initialization. Defaults to False.
        """

        self._path = path
        self._enabled = True

        self._backend = SQLiteBackend(
            cache_name=Client.path_create(path),
            expire_after=expire_after,
            allowed_methods=("GET"),
            include_headers=True,
        )

        self._session = CachedSession(cache=self._backend)

        if force_clear:
            await self._session.cache.clear()

        if clear_expired:
            await self._session.cache.delete_expired_responses()

    async def cache_disable(self) -> None:
        """Disable caching"""
        self._enabled = False
        self._session = ClientSession()

    async def _get(self, url: str) -> dict:
        """Make an asynchronous HTTP GET request to the provided URL.
        Args:
            url (str): The URL to make the GET request to.
        Returns:
            dict: The JSON response of the GET request.
        Raises:
            HTTPError: If the response status is 400 or higher.
        """
        async with self._session.get(url) as response:
            return await response.json()

    async def close(self) -> None:
        """Close the session and releases all resources held by the session."""
        await self._session.close()

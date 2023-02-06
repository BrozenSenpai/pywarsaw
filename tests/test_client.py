import pytest
import aioresponses
from aiohttp import ClientSession, ClientResponse
from aiohttp_client_cache import CachedSession, SQLiteBackend, CachedResponse

from pywarsaw.client import Client
from pywarsaw.exceptions import WrongDirectory


def test_path_create():
    output = "tests/resources/pywarsaw_cache"
    assert Client.path_create("tests/resources") == output
    assert Client.path_create("tests/resources/") == output


def test_path_create_wrong_dir():
    with pytest.raises(WrongDirectory):
        Client.path_create("tests/charizard")


@pytest.mark.asyncio
async def test_cache_enable_creates_sqlite_backed():
    client = Client()
    await client.cache_enable(path="./tests/resources/")
    assert isinstance(client.backend, SQLiteBackend)
    await client.close()


@pytest.mark.asyncio
async def test_cache_enable_creates_cached_session():
    client = Client()
    await client.cache_enable()
    assert isinstance(client.session, CachedSession)
    await client.close()


@pytest.mark.asyncio
async def test_cache_disable_creates_client_session():
    client = Client()
    await client.cache_disable()
    assert isinstance(client.session, ClientSession)
    await client.close()


@pytest.mark.asyncio
async def test_get_without_caching():
    with aioresponses.aioresponses() as m:
        client = Client()
        await client.cache_disable()
        m.get("http://example.com", payload=dict(name="squirtle"))
        response = await client._get("http://example.com")
        assert response == dict(name="squirtle")
        await client.close()


@pytest.mark.asyncio
async def test_get_with_caching():
    with aioresponses.aioresponses() as m:
        client = Client()
        await client.cache_enable(path="./tests/resources/", force_clear=True)
        m.get("http://example.com", payload=dict(name="charmander"))
        response = await client._get("http://example.com")
        assert response == dict(name="charmander")
        await client.close()

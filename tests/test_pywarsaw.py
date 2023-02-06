import pytest
import aioresponses

from pywarsaw import __version__
from pywarsaw.pywarsaw import Mermaid
from pywarsaw.exceptions import WrongQueryParameters, WrongAPIKey, UnauthorizedAccess


def test_version():
    assert __version__ == "0.1.0"


def test_build_url():
    url = "https://api.um.warszawa.pl/api/action/endpoint_test?test1=test1&test2=test2"
    assert Mermaid._build_url(endpoint="endpoint_test", test1="test1", test2="test2")


@pytest.mark.asyncio
async def test_get_data_with_wrong_query_parameters():
    with aioresponses.aioresponses() as m:
        client = Mermaid()
        await client.cache_disable()
        m.get(
            "http://example.com",
            payload=dict(result="Błędna metoda lub parametry wywołania"),
        )
        with pytest.raises(WrongQueryParameters):
            await client._get_data("http://example.com")
        await client.close()


@pytest.mark.asyncio
async def test_get_data_with_wrong_api_key():
    with aioresponses.aioresponses() as m:
        client = Mermaid()
        await client.cache_disable()
        m.get(
            "http://example.com",
            payload=dict(result="false", error="Błędny apikey lub jego brak"),
        )
        with pytest.raises(WrongAPIKey):
            await client._get_data("http://example.com")
        await client.close()


@pytest.mark.asyncio
async def test_get_data_with_unauthorized_access():
    with aioresponses.aioresponses() as m:
        client = Mermaid()
        await client.cache_disable()
        m.get(
            "http://example.com",
            payload=dict(result="false", error="Nieautoryzowany dostęp do danych"),
        )
        with pytest.raises(UnauthorizedAccess):
            await client._get_data("http://example.com")
        await client.close()

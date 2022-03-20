from dotenv import load_dotenv
from SPARQLWrapper import SPARQLWrapper

import os

from .queries import Query

load_dotenv()
TRIPLE_STORE_URL: str = os.getenv("TRIPLE_STORE_URL","http://127.0.0.1:3030")


def fetch_data(query: Query, endpoint: str = f"{TRIPLE_STORE_URL}/bicycle") -> dict:
    """ Fetches data from the triple store.
    :param query: The query to execute.
    :param endpoint: The endpoint to query. Defaults to the triple store.
    :return: The data returned from the query.
    """
    client: SPARQLWrapper = SPARQLWrapper(endpoint)
    client.setQuery(query.value)
    client.setReturnFormat('json')
    return client.queryAndConvert()


def get_all_stations() -> dict:
    """Returns all stations from the triple store.
    :return: The data returned from the query.
    """
    url: str = f"{TRIPLE_STORE_URL}/bicycle"
    return fetch_data(query=Query.ALL_STATIC_STATIONS, endpoint=url)

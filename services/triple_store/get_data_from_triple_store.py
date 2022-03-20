from dotenv import load_dotenv
from SPARQLWrapper import SPARQLWrapper

import os

from .queries import Query

load_dotenv()
TRIPLE_STORE_URL: str = os.getenv("TRIPLE_STORE_URL")


def fetch_data(endpoint: str, query: str) -> dict:
    """ Fetches data from the triple store.
    :param endpoint: The endpoint to query.
    :param query: The query to execute.
    :return: The data returned from the query.
    """
    client: SPARQLWrapper = SPARQLWrapper(endpoint)
    client.setQuery(query)
    client.setReturnFormat('json')
    return client.queryAndConvert()


def get_all_stations() -> dict:
    """Returns all stations from the triple store.
    :return: The data returned from the query.
    """
    url: str = f"{TRIPLE_STORE_URL}/bicycle"
    return fetch_data(url, Query.ALL_STATIONS.value)

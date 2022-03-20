from dotenv import load_dotenv
from SPARQLWrapper import SPARQLWrapper

import os

from .queries import Query

load_dotenv()
TRIPLE_STORE_URL: str = os.getenv("TRIPLE_STORE_URL")


def fetch_data(endpoint: str, query: str) -> dict:
    """Returns the result of a SPARQL query.

    Keyword arguments:
    endpoint - URL of sparql endpoint
    query    - SPARQL query to be executed
    """
    client: SPARQLWrapper = SPARQLWrapper(endpoint)
    client.setQuery(query)
    client.setReturnFormat('json')
    return client.queryAndConvert()


def get_all_stations() -> dict:
    url: str = f"{TRIPLE_STORE_URL}/bicycle"
    return fetch_data(url, Query.ALL_STATIONS.value)

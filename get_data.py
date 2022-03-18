from SPARQLWrapper import SPARQLWrapper, CSV, JSON
from flask import jsonify
from collections import defaultdict

def get_data(endpoint, query):
    """Returns the result and mimetype of executing the given query against 
    the given endpoint.

    Keyword arguments:
    endpoint - URL of sparql endpoint
    query    - SPARQL query to be executed
    """
    client = SPARQLWrapper(endpoint)
    client.setQuery(query)
    client.setReturnFormat('json')
    #client.setCredentials(static.DEFAULT_ENDPOINT_USER, static.DEFAULT_ENDPOINT_PASSWORD)
    result = client.queryAndConvert()

    return result
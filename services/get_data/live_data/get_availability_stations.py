from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import XSD
import requests
from dotenv import load_dotenv

import os

load_dotenv()
schema: Namespace = Namespace(os.getenv("ONTOLOGY_URL"))


def get_availability_stations(
        url: str = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q"
                   "=&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet"
                   "=nom_arrondissement_communes&rows=2000") -> Graph:
    """ Get the availability of the stations
    :param url: the url of the API
    :return: the graph with the data
    """
    response: requests.Response = requests.get(url)
    response_json: dict = response.json()
    records: list = response_json['records']

    g: Graph = Graph()
    live_station: Namespace = Namespace(f'{schema}/live_bicycle_station/')

    for record in records:
        g.add((URIRef(live_station + record['fields']['stationcode']), RDF.type, URIRef(f"{schema}/station")))
        g.add(
            (URIRef(live_station + record['fields']['stationcode']), URIRef(f"{schema}/id"),
             Literal(record['fields']['stationcode'], datatype=XSD.integer))
        )
        g.add(
            (URIRef(live_station + record['fields']['stationcode']), URIRef(f"{schema}/name"),
             Literal(record['fields']['name'], datatype=XSD.string))
        )
        g.add(
            (URIRef(live_station + record['fields']['stationcode']), URIRef(f"{schema}/nb_electrical_bicycles"),
             Literal(record['fields']['ebike'], datatype=XSD.integer))
        )
        g.add(
            (URIRef(live_station + record['fields']['stationcode']), URIRef(f"{schema}/nb_mechanical_bicycles"),
             Literal(record['fields']['mechanical'], datatype=XSD.integer))
        )
        g.add(
            (URIRef(live_station + record['fields']['stationcode']), URIRef(f"{schema}/update_date"),
             Literal(record['fields']['duedate'], datatype=XSD.string))
        )
        g.add(
            (URIRef(live_station + record['fields']['stationcode']), URIRef(f"{schema}/nb_available_terminals"),
             Literal(record['fields']['numdocksavailable'], datatype=XSD.integer))
        )
        g.add(
            (URIRef(live_station + record['fields']['stationcode']), URIRef(f"{schema}/has_payment_terminal"),
             Literal(record['fields']['is_renting'] == 'OUI', datatype=XSD.boolean))
        )
        g.add(
            (URIRef(live_station + record['fields']['stationcode']), URIRef(f"{schema}/is_usable"),
             Literal(record['fields']['is_installed'] == 'OUI', datatype=XSD.boolean))
        )
        g.add(
            (URIRef(live_station + record['fields']['stationcode']), URIRef(f"{schema}/commune"),
             Literal(record['fields']['nom_arrondissement_communes'], datatype=XSD.string))
        )
        g.add(
            (URIRef(live_station + record['fields']['stationcode']), URIRef(f"{schema}/can_return_bicycle"),
             Literal(record['fields']['is_returning'] == 'OUI', datatype=XSD.boolean))
        )

    return g

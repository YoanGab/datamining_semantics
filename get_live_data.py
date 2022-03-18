import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import XSD
import requests

schema: Namespace = Namespace('http://www.semanticweb.org/groupe1/ontologies/2022/2')

def get_live_data(url: str = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes") -> Graph:
    response: requests.Response = requests.get(url)
    response_json: dict = response.json()
    records: list = response_json['records']
    g: Graph = Graph()
    live_station: Namespace = Namespace(f'{schema}/live_bicycle_station/')

    for record in records:
        g.add((URIRef(live_station + record['fields']['stationcode']), RDF.type, URIRef(f"{schema}/station")))
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
             Literal(record['fields']['duedate'], datatype=XSD.integer))
        )
        g.add(
            (URIRef(live_station + record['fields']['stationcode']), URIRef(f"{schema}/nb_available_terminals"),
             Literal(record['fields']['numdocksavailable'], datatype=XSD.integer))
        )
        g.add(
            (URIRef(live_station + record['fields']['stationcode']), URIRef(f"{schema}/has_payment_terminal"),
             Literal(record['fields']['is_renting'], datatype=XSD.integer))
        )
        g.add(
            (URIRef(live_station + record['fields']['stationcode']), URIRef(f"{schema}/is_usable"),
             Literal(record['fields']['is_installed'], datatype=XSD.integer))
        )
        g.add(
            (URIRef(live_station + record['fields']['stationcode']), URIRef(f"{schema}/commune"),
             Literal(record['fields']['nom_arrondissement_communes'], datatype=XSD.integer))
        )
        g.add(
            (URIRef(live_station + record['fields']['stationcode']), URIRef(f"{schema}/can_return_bicycle"),
             Literal(record['fields']['is_returning'], datatype=XSD.integer))
        )

    return g

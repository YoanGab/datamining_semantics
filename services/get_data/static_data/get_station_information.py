import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import XSD
from dotenv import load_dotenv

import os

load_dotenv()
schema: Namespace = Namespace(os.getenv("ONTOLOGY_URL"))


def get_station_information(csv_path: str = './data/velib-emplacement-des-stations.csv', sep=';') -> Graph:
    df: pd.DataFrame = pd.read_csv(csv_path, sep=sep)
    df['latitude'] = df['Coordonnées géographiques'].str.split(',').str[0]
    df['longitude'] = df['Coordonnées géographiques'].str.split(',').str[1]
    g: Graph = Graph()
    station: Namespace = Namespace(f'{schema}/bicycle_station/')

    for index, row in df.iterrows():
        g.add((URIRef(station + row['Identifiant station']), RDF.type, URIRef(f"{schema}/station")))
        g.add(
            (URIRef(station + row['Identifiant station']), URIRef(f"{schema}/id"),
             Literal(row['Identifiant station'], datatype=XSD.integer))
        )
        g.add(
            (URIRef(station + row['Identifiant station']), URIRef(f"{schema}/name"),
             Literal(row['Nom de la station'], datatype=XSD.string))
        )
        g.add(
            (URIRef(station + row['Identifiant station']), URIRef(f"{schema}/capacity"),
             Literal(row['Capacité de la station'], datatype=XSD.integer))
        )
        g.add(
            (URIRef(station + row['Identifiant station']), URIRef(f"{schema}/latitude"),
             Literal(row['latitude'], datatype=XSD.double))
        )
        g.add(
            (URIRef(station + row['Identifiant station']), URIRef(f"{schema}/longitude"),
             Literal(row['longitude'], datatype=XSD.double))
        )

    return g

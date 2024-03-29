from __future__ import annotations

import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()
PREFIX: str = f"PREFIX ns1:<{os.getenv('ONTOLOGY_URL', 'http://www.semanticweb.org/groupe1/ontologies/2022/2')}/>"


class Query(Enum):
    """ Enum class for all the queries """

    ALL_STATIC_STATIONS: Query = f"""
        {PREFIX}
        SELECT ?id ?name ?latitude ?longitude ?capacity
        WHERE {{
            ?sta ns1:id ?id .
            ?sta ns1:name ?name .
            ?sta ns1:longitude ?longitude .
            ?sta ns1:latitude ?latitude .
            ?sta ns1:capacity ?capacity .
        }}
    """

    ALL_LIVE_STATIONS: Query = f"""
        {PREFIX}
        SELECT ?id ?name ?nb_electrical_bicycles ?nb_mechanical_bicycles ?update_date ?nb_available_terminals ?has_payment_terminal ?is_usable ?commune ?can_return_bicycle
        WHERE {{
            ?sta ns1:id ?id .
            ?sta ns1:name ?name .
            ?sta ns1:nb_electrical_bicycles ?nb_electrical_bicycles .
            ?sta ns1:nb_mechanical_bicycles ?nb_mechanical_bicycles .
            ?sta ns1:update_date ?update_date .
            ?sta ns1:nb_available_terminals ?nb_available_terminals .
            ?sta ns1:has_payment_terminal ?has_payment_terminal .
            ?sta ns1:is_usable ?is_usable .
            ?sta ns1:commune ?commune .
            ?sta ns1:can_return_bicycle ?can_return_bicycle .
        }}
    """

    ALL_ELECTRIC_LIVE_STATIONS_AVAILABLE: Query = f"""
        {PREFIX}
        SELECT ?id ?name ?nb_electrical_bicycles ?nb_mechanical_bicycles ?update_date ?nb_available_terminals ?has_payment_terminal ?is_usable ?commune ?can_return_bicycle
        WHERE {{
            ?sta ns1:id ?id .
            ?sta ns1:name ?name .
            ?sta ns1:nb_electrical_bicycles ?nb_electrical_bicycles .
            ?sta ns1:nb_mechanical_bicycles ?nb_mechanical_bicycles .
            ?sta ns1:update_date ?update_date .
            ?sta ns1:nb_available_terminals ?nb_available_terminals .
            ?sta ns1:has_payment_terminal ?has_payment_terminal .
            ?sta ns1:is_usable ?is_usable .
            ?sta ns1:commune ?commune .
            ?sta ns1:can_return_bicycle ?can_return_bicycle .
            FILTER (?nb_electrical_bicycles > 0)
        }}
    """

    ALL_MECHANICAL_LIVE_STATIONS_AVAILABLE: Query = f"""
        {PREFIX}
        SELECT ?id ?name ?nb_electrical_bicycles ?nb_mechanical_bicycles ?update_date ?nb_available_terminals ?has_payment_terminal ?is_usable ?commune ?can_return_bicycle
        WHERE {{
            ?sta ns1:id ?id .
            ?sta ns1:name ?name .
            ?sta ns1:nb_electrical_bicycles ?nb_electrical_bicycles .
            ?sta ns1:nb_mechanical_bicycles ?nb_mechanical_bicycles .
            ?sta ns1:update_date ?update_date .
            ?sta ns1:nb_available_terminals ?nb_available_terminals .
            ?sta ns1:has_payment_terminal ?has_payment_terminal .
            ?sta ns1:is_usable ?is_usable .
            ?sta ns1:commune ?commune .
            ?sta ns1:can_return_bicycle ?can_return_bicycle .
            FILTER (?nb_mechanical_bicycles > 0)
        }}
    """

    ALL_LIVE_STATIONS_AVAILABLE: Query = f"""
        {PREFIX}
        SELECT ?id ?name ?nb_electrical_bicycles ?nb_mechanical_bicycles ?update_date ?nb_available_terminals ?has_payment_terminal ?is_usable ?commune ?can_return_bicycle
        WHERE {{
            ?sta ns1:id ?id .
            ?sta ns1:name ?name .
            ?sta ns1:nb_electrical_bicycles ?nb_electrical_bicycles .
            ?sta ns1:nb_mechanical_bicycles ?nb_mechanical_bicycles .
            ?sta ns1:update_date ?update_date .
            ?sta ns1:nb_available_terminals ?nb_available_terminals .
            ?sta ns1:has_payment_terminal ?has_payment_terminal .
            ?sta ns1:is_usable ?is_usable .
            ?sta ns1:commune ?commune .
            ?sta ns1:can_return_bicycle ?can_return_bicycle .
            FILTER (?nb_electrical_bicycles > 0 || ?nb_mechanical_bicycles > 0)
        }}
    """

    ALL_LIVE_STATIONS_AVAILABLE_FOR_RETURN: Query = f"""
        {PREFIX}
        SELECT ?id ?name ?nb_electrical_bicycles ?nb_mechanical_bicycles ?update_date ?nb_available_terminals ?has_payment_terminal ?is_usable ?commune ?can_return_bicycle
        WHERE {{
            ?sta ns1:id ?id .
            ?sta ns1:name ?name .
            ?sta ns1:nb_electrical_bicycles ?nb_electrical_bicycles .
            ?sta ns1:nb_mechanical_bicycles ?nb_mechanical_bicycles .
            ?sta ns1:update_date ?update_date .
            ?sta ns1:nb_available_terminals ?nb_available_terminals .
            ?sta ns1:has_payment_terminal ?has_payment_terminal .
            ?sta ns1:is_usable ?is_usable .
            ?sta ns1:commune ?commune .
            ?sta ns1:can_return_bicycle ?can_return_bicycle .
            FILTER (?nb_available_terminals > 0)
        }}
    """

    """
    SPARQL queries
    """

    STATIC_STATION_GRAPH_PATTERN: Query = f"""
        {PREFIX}
        SELECT ?sta
        WHERE {{
            ?sta a ns1:station
        }}
    """

    # Return true if there is a station named "Château - République"
    STATIC_STATION_ASK: Query = f"""
        {PREFIX}
        ASK{{ ?sta ns1:name \"Château - République\" .}}
    """

    # Describe the station "Château - République" with each subject, predicate and object for this station
    STATIC_STATION_DESCRIBE: Query = f"""{PREFIX}
        DESCRIBE ?sta 
        WHERE {{
        ?sta ns1:name "Château - République" .
        }}
    """

    # Create a new table RDF with only name and capacity
    STATIC_CREATE_RDF_NAME_CAPACITY: Query = f"""{PREFIX}
    CONSTRUCT {{ ?sta ns1:name ?name . ?sta ns1:capacity ?cap .}}
    WHERE 
    {{
        ?sta ns1:name ?name .
        ?sta ns1:capacity ?cap
    }}
    """

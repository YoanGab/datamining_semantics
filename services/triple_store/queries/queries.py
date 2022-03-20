from dotenv import load_dotenv

from enum import Enum
import os

load_dotenv()
PREFIX: str = f"PREFIX ns1:<{os.getenv('ONTOLOGY_URL')}/>"


class Query(Enum):
    """ Enum class for all the queries
    """
    ALL_STATIC_STATIONS: str = f"""
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

    ALL_LIVE_STATIONS: str = f"""
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

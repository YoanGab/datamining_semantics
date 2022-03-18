from enum import Enum

PREFIX = "PREFIX ns1:<http://www.semanticweb.org/groupe1/ontologies/2022/2/>"


class Queries(Enum):
    ALL_STATION = PREFIX + """SELECT DISTINCT
        ?name ?latitude ?longitude ?capacity
        WHERE {
            ?sta ns1:name ?name .
            ?sta ns1:longitude ?longitude .
            ?sta ns1:latitude ?latitude .
            ?sta ns1:capacity ?capacity .
        } LIMIT 500"""

from dotenv import load_dotenv
from flask import Flask, render_template, request
import rdflib

import os

import services.get_data as get_data
import services.triple_store as triple_store
from services.triple_store.queries import Query

load_dotenv()
app = Flask(__name__, template_folder='./templates', static_folder='./templates/assets/common')


# def _convert_static_item_to_dict(item: rdflib.query.ResultRow) -> dict:
#     """ Convert the static data to a dict
#     :param item: the static data
#     :return: dict containing the data for the station given in parameter
#     """
#     return {
#         'id': item['id']['value'] if item['id'] else '',
#         'name': item['name']['value'] if item['name'] else '',
#         'latitude': float(item['latitude']['value']),
#         'longitude': float(item['longitude']['value']),
#         'capacity': int(item['capacity']['value']) if item['capacity'] else 0,
#     }
#
#
# def get_static_data_parsed(query: Query = Query.ALL_STATIC_STATIONS) -> list[dict]:
#     """ Get the static data from the triple store
#     :param query: the query to use
#     :return: list of dict containing the data for the stations (static)
#     """
#     result: dict = triple_store.fetch_data(query=query)
#
#     bulk: list = []
#     for row in result['results']['bindings']:
#         bulk.append(_convert_static_item_to_dict(row))
#     return bulk
def _convert_static_item_to_dict(item: rdflib.query.ResultRow) -> dict:
    """ Convert the static data to a dict
    :param item: the static data
    :return: dict containing the data for the station given in parameter
    """
    return {
        'id': item.id.value,
        'name': item.name.value if item.name else '',
        'capacity': item.capacity.value if item.capacity else 0,
        'latitude': item.latitude.value,
        'longitude': item.longitude.value
    }


def get_static_data_parsed(query: Query = Query.ALL_STATIC_STATIONS) -> list[dict]:
    """ Get the static data from the triple store
    :param query: the query to use
    :return: list of dict containing the data for the stations (static)
    """
    data: rdflib.Graph = get_data.get_station_information()
    result: rdflib.query.Result = data.query(query_object=query.value)

    #result: rdflib.Graph = triple_store.get_all_stations()

    bulk: list = []
    for row in result:
        bulk.append(_convert_static_item_to_dict(row))
    return bulk

def _convert_live_item_to_dict(item: rdflib.query.ResultRow) -> dict:
    """ Convert the live data to a dict
    :param item: the live data
    :return: dict containing the data for the station given in parameter
    """
    update_date_str: str = item.update_date.value
    from datetime import datetime
    if update_date_str:
        update_date = datetime.strptime(update_date_str, '%Y-%m-%dT%H:%M:%S+00:00')
        update_date_str = update_date.strftime('%d/%m/%Y %H:%M')
    else:
        update_date_str = '-'

    return {
        'id': item.id.value,
        'name': item.name.value if item.name else '',
        'nb_electrical_bicycles': int(item.nb_electrical_bicycles.value) if item.nb_electrical_bicycles else 0,
        'nb_mechanical_bicycles': int(item.nb_mechanical_bicycles.value) if item.nb_mechanical_bicycles else 0,
        'update_date': update_date_str,
        'nb_available_terminals': item.nb_available_terminals.value if item.nb_available_terminals else 0,
        'has_payment_terminal': item.has_payment_terminal.value if item.has_payment_terminal else False,
        'is_usable': item.is_usable.value if item.is_usable else False,
        'commune': item.commune.value if item.commune else '',
        'can_return_bicycle': item.can_return_bicycle.value if item.can_return_bicycle else False,
    }


def get_live_data_parsed(query: Query = Query.ALL_LIVE_STATIONS) -> list[dict]:
    """ Get the live data from the triple store
    :param query: the query to use
    :return: list of dict containing the data for the stations (live)
    """
    data: rdflib.Graph = get_data.get_availability_stations()
    result: rdflib.query.Result = data.query(query_object=query.value)
    bulk: list = []
    for row in result:
        bulk.append(_convert_live_item_to_dict(row))
    return bulk


def get_station_data(static_query: Query = Query.ALL_STATIC_STATIONS, live_query: Query = Query.ALL_LIVE_STATIONS) -> list:
    """ Get the data from the static and live data
    :param static_query: the query to use for the static data
    :param live_query: the query to use for the live data
    :return: list of dict containing the data for the stations (static and live)
    """
    live_data: list = get_live_data_parsed(query=live_query)
    static_data: list = get_static_data_parsed(query=static_query)
    merged_data: list = []
    for live_item in live_data:
        for static_item in static_data:
            if live_item['id'] == static_item['id']:
                merged_data.append(dict(live_item, **static_item))
    return merged_data


@app.route('/', methods=['GET', 'POST'])
def index():
    mapbox_access_token: str = os.getenv('MAPBOX_ACCESS_TOKEN')
    if request.method == 'GET':
        data: list = get_station_data()
        return render_template('index.html', data=data, mapbox_access_token=mapbox_access_token)

    static_query: Query = Query.ALL_STATIC_STATIONS
    if request.form['type_of_bicycle'] == 'electric':
        live_query: Query = Query.ALL_ELECTRIC_LIVE_STATIONS_AVAILABLE
    else:
        live_query: Query = Query.ALL_MECHANICAL_LIVE_STATIONS_AVAILABLE
    data: list = get_station_data(static_query=static_query, live_query=live_query)

    return render_template('index.html', data=data, mapbox_access_token=mapbox_access_token)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)

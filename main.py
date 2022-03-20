import os

import rdflib.query
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_minify import minify
from rdflib import Graph

import services.get_data as get_data
from services.triple_store.queries import Query

load_dotenv()
app = Flask(__name__)
minify(app=app, html=True, js=True, cssless=True)


def _convert_static_item_to_dict(item: rdflib.query.ResultRow) -> dict:
    return {
        'id': item.id.value,
        'name': item.name.value if item.name else '',
        'capacity': item.capacity.value if item.capacity else 0,
        'latitude': item.latitude.value,
        'longitude': item.longitude.value
    }


def get_static_data_parsed() -> list[dict]:
    data: Graph = get_data.get_station_information()
    result: rdflib.query.Result = data.query(Query.ALL_STATIC_STATIONS.value)
    bulk: list = []
    for row in result:
        bulk.append(_convert_static_item_to_dict(row))
    return bulk


def _convert_live_item_to_dict(item: rdflib.query.ResultRow) -> dict:
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


def get_live_data_parsed() -> list[dict]:
    data: Graph = get_data.get_availability_stations()
    result: rdflib.query.Result = data.query(Query.ALL_LIVE_STATIONS.value)
    bulk: list = []
    for row in result:
        bulk.append(_convert_live_item_to_dict(row))
    return bulk


def get_station_data() -> list:
    live_data: list = get_live_data_parsed()
    static_data: list = get_static_data_parsed()
    merged_data: list = []
    for live_item in live_data:
        for static_item in static_data:
            if live_item['id'] == static_item['id']:
                merged_data.append(dict(live_item, **static_item))
    return merged_data


@app.route('/', methods=['GET', 'POST'])
def index():
    access_token: str = os.getenv('ACCESS_TOKEN')
    data: list = get_station_data()
    return render_template('index.html', data=data, access_token=access_token)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)

import re
from flask import Flask, render_template, request
from flask_minify import minify
from rdflib import Graph, Literal
from rdflib.plugins.sparql import prepareQuery
from JSONLD import *
from Queries import *

app = Flask(__name__)
minify(app=app, html=True, js=True, cssless=True)

velib_api = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes"

velib_api_context = r'contexts/velib_api_context.json'

velib_api_json = JSONLD(velib_api_context, velib_api)

######################################
# GENERATE GRAPH
######################################
g = Graph()
g.parse(data=velib_api_json, format="json-ld")


# Parse data to return to the view
def parse_data(item):
    regex = re.match('^http', item.isElectrical.value)
    isElectrical = False if regex is None else True
    record = {
        "address": item.add.value.replace('\n\r', ' ').replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' '),
        "zipcode": item.zipcode.value,
        "lat": item.lat.value,
        "lon": item.lon.value,
        "isElectrical": isElectrical,
        "name": "" if item.name is None else item.name.value,
        "services": "" if item.services is None else item.services.value.replace('|', ', '),
        "city": "" if item.city is None else item.city.value,
        "fuel": "" if item.fuel is None else item.fuel.value.replace('|', ', '),
        "paying": "" if item.isPayant is None else item.isPayant.value,
        "numberPlugs": "" if item.numberPlugs is None else item.numberPlugs.value,
    }
    return record


# Check filters for searchbar : return the query
def check_filters():
    if request.form.get('type_of_car'):
        checked = request.form.getlist('type_of_car')

        if 'electric' in checked and 'thermic' not in checked:
            query = Queries.ELECTRIC_CARS_ONLY.value

        elif 'thermic' in checked and 'electric' not in checked:
            query = Queries.THERMIC_CARS_ONLY.value

        else:
            query = Queries.ALL_CARS.value

    else:
        query = Queries.ALL_CARS.value

    return query


@app.route('/', methods=['GET', 'POST'])
def index():
    zipcode_query = Queries.ALL_ZIPCODES.value
    query = Queries.ALL_CARS.value
    data = []
    all_zipcodes = []

    for _ in g.query(zipcode_query):
        all_zipcodes.append(_.zipcode.value)

    if request.method == 'POST':
        if request.form['search']:
            code = Literal(request.form['search'])
            query = check_filters()
            q = prepareQuery(query)

            for item in g.query(q, initBindings={'zipcode': code}):
                data.append(parse_data(item))

        else:
            query = check_filters()

            for item in g.query(query):
                data.append(parse_data(item))

    else:
        for item in g.query(query):
            data.append(parse_data(item))

    return render_template('index.html', all_zipcodes=all_zipcodes, data=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# if __name__ == '__main__':
#     app.run(port="5000", debug=True)

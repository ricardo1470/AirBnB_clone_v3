#!/usr/bin/python3
"""Flask Cities"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False)
def get_all_cities(state_id):
    """Retrieves the list of all City objects of a State"""

    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    cities = []
    for mv in state.cities:
        cities.append(mv.to_dict())
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    """Retrieves a City object"""
    city = storage.get(City, city_id)

    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""

    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City"""

    state = storage.get("State", state_id)

    if state is None:
        abort(404)

    json_input = request.get_json(silent=True)

    if not json_input:
        abort(400, "Not a JSON")

    try:
        nm = json_input['name']
    except KeyError:
        abort(400, "Missing name")

    json_input['state_id'] = state.id
    new_city = City(**json_input)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Updates a City object"""

    cityID = storage.get('City', city_id)

    if cityID is None:
        abort(404)

    json_input = request.get_json()
    if json_input is None:
        abort(400, "Not a JSON")

    for key, value in json_input.items():
        setattr(cityID, key, value)

    storage.save()
    return jsonify(cityID.to_dict()), 200

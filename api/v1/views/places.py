#!/usr/bin/python3
"""Flask Places"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """Retrieves the list of all Place objects of a City"""

    placeID = storage.get("City", city_id)
    if placeID is None:
        abort(404)
    place_dic = []
    for placeID in placeID.places:
        place_dic.append(placeID.to_dict())
    return jsonify(place_dic)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_places(place_id):
    """Deletes a Place object"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""

    if not storage.get("City", city_id):
        abort(404)

    json_input = request.get_json()

    if not json_input:
        abort(400, 'Not a JSON')

    if "user_id" not in data:
        abort(400, 'Missing user_id')

    if storage.get("User", json_input["user_id"]) is None:
        abort(404)

    if "name" not in json_input:
        abort(400, 'Missing name')

    new = Place(user_id=json_input["user_id"],
                name=json_input["name"],
                city_id=city_id)
    storage.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_a_places(place_id):
    """Updates a Place object"""

    places = list(storage.all(Place).values())

    json_input = request.get_json(silent=True)

    if json_input is None:
        return make_response("Not a JSON", 400)

    for mv in places:
        if mv.id == place_id:
            for key, value in json_input.items():
                if key != 'id' and key != 'created_at' and key != 'updated_at'\
                        and key != 'user_id' and key != 'city_id':
                    setattr(mv, key, value)

            storage.save()
            return jsonify(mv.to_dict()), 200
    abort(404)

#!/usr/bin/python3
"""Flask Amenities"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage, amenity
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""

    amen = []
    for mv in storage.all("Amenity").values():
        amen.append(mv.to_dict())
    return jsonify(amen)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """Retrieves a Amenity object"""

    amen = storage.get("Amenity", amenity_id)
    if amen is None:
        abort(404)
    else:
        return jsonify(amen.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """Deletes a Amenity object"""

    amen = storage.get("Amenity", amenity_id)

    if amen is None:
        abort(404)
    else:
        storage.delete(amen)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a Amenity"""

    json_input = request.get_json(silent=True)

    if json_input is None:
        abort(400, "Not a JSON")

    try:
        nm = json_input['name']
    except KeyError:
        abort(400, "Missing name")

    newAmen = Amenity(**json_input)
    storage.new(newAmen)
    storage.save()
    return jsonify(newAmen.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Updates a Amenity object"""

    amen = storage.get("Amenity", amenity_id)

    if amen is None:
        abort(404)

    json_input = request.get_json()

    if json_input is None:
        abort(400, "Not a JSON")

    for key, value in json_input.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(amen, key, value)
    storage.save()
    return jsonify(amen.to_dict()), 200

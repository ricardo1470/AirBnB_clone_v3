#!/usr/bin/python3
"""Flask Users"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage, user
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    users = []
    for mv in storage.all("User").values():
        users.append(mv.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    """Retrieves a User object"""

    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    """Deletes a User object"""

    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""

    json_input = request.get_json(silent=True)

    if json_input is None:
        abort(400, "Not a JSON")

    if 'email' not in json_input:
        abort(400, 'Missing email')

    if 'password' not in json_input:
        abort(400, 'Missing password')

    Nusr = User(**json_input)
    Nusr.save()
    return jsonify(Nusr.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""

    user = storage.get("User", user_id)

    if user is None:
        abort(404)

    json_input = request.get_json()

    if json_input is None:
        abort(400, "Not a JSON")

    for key, value in json_input.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())

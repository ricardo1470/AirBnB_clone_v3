#!/usr/bin/python3
"""Flask States"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrieves the list of all State objects"""

    states_list = list(storage.all(State).values())
    states_dic = []

    for mv in states_list:
        state_dict = mv.to_dict()
        states_dic.append(state_dict)
    return jsonify(states_dic)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""

    StateID = storage.get(State, state_id)

    if StateID is not None:
        return jsonify(StateID.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """Deletes a State object"""

    stateID = storage.get(State, state_id)

    if stateID is not None:
        storage.delete(stateID)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""

    json_input = request.get_json(silent=True)

    if json_input is None:
        abort(400, "Not a JSON")

    try:
        state_name = json_input['name']
    except KeyError:
        abort(400, "Missing name")

    new_state = State(name=state_name)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Updates a State object"""

    stateID = storage.get(State, state_id)

    if stateID is None:
        abort(404)

    json_input = request.get_json()

    if json_input is None:
        abort(400, "Not a JSON")

    for key, value in json_input.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(stateID, key, value)
    storage.save()
    return jsonify(stateID.to_dict()), 200

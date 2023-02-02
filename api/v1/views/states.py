#!/usr/bin/python3
""" states API view """
from flask import Blueprint, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', strict_slashes=False)
def all_states():
    """ Retrieves all states """
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a particular state by its <state_id> """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Delete state by ID and return empty JSON in its place """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """ Create a new state """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_state = State(**request.get_json())
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_State(state_id=None):
    """ Update state by <state_id> """
    state_to_update = storage.get(State, state_id)
    req = request.get_json()

    if state_to_update is None:
        abort(404)
    if req is None:
        abort(400)
    for key, value in req.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_to_update, key, value)
    storage.save()
    return jsonify(state_to_update.to_dict())

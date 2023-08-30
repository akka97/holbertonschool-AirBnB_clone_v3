#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    retrieves all State objects
    :return: json of all states
    """
    state_list = []
    state_obj = storage.all(State).values()
    for obj in state_obj:
        state_list.append(obj.to_dict())

    return jsonify(state_list)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    create state route
    :return: newly created state obj
    """
    if not request.get_json():
        abort(400, 'Not a JSON')
    if "name" not in request.get_json():
        abort(400, 'Missing name')

    data = request.get_json()
    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    gets a specific State object by ID
    :param state_id: state object id
    :return: state obj with the specified id or error
    """

    fetched_obj = storage.get(State, state_id)

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_dict())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    updates specific State object by ID
    :param state_id: state object ID
    :return: state object and 200 on success, or 400 or 404 on failure
    """
    fetched_obj = storage.get(State, state_id)
    state_json = request.get_json()
    if fetched_obj is None:
        abort(404, 'Not a JSON')
    if state_json is None:
        abort(400)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """
    deletes State by id
    :param state_id: state object id
    :return: empty dict with 200 or 404 if not found
    """

    fetched_obj = storage.get(State, state_id)

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()
    return jsonify({})

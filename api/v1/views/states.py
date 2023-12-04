#!/usr/bin/python3
"""This is the State module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get.yml', methods=['GET'])
def get_all():
    """Get all values by id"""
    all_vals = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(all_vals)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/state/get_id.yml', methods=['GET'])
def get_method_state(state_id):
    """Get state(s) by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/delete.yml', methods=['DELETE'])
def del_method(state_id):
    """Delete state(s) by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/state/post.yml', methods=['POST'])
def create_obj():
    """Create a new instance"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    js_req = request.get_json()
    obj = State(**js_req)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/state/put.yml', methods=['PUT'])
def post_method(state_id):
    """Update state by id"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    contnt = storage.get(State, state_id)
    if contnt is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(contnt, key, value)
    storage.save()
    return jsonify(contnt.to_dict())

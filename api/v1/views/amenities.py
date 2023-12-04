#!/usr/bin/python3
"""
This is the Amenity module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity
from flasgger.utils import swag_from


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/get.yml', methods=['GET'])
def get_all_amenities():
    """Get all amenities by id """
    all_amenities = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(all_amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/amenity/get_id.yml', methods=['GET'])
def get_amenity(amenity_id):
    """Get amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/amenity/delete.yml', methods=['DELETE'])
def del_amenity(amenity_id):
    """Delete amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/amenity/post.yml', methods=['POST'])
def create_obj_amenity():
    """Create new instance """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    js_req = request.get_json()
    new_obj = Amenity(**js_req)
    new_obj.save()
    return (jsonify(new_obj.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/amenity/put.yml', methods=['PUT'])
def post_amenity(amenity_id):
    """This is the post method"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    contnt = storage.get(Amenity, amenity_id)
    if contnt is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(contnt, key, value)
    storage.save()
    return jsonify(contnt.to_dict())

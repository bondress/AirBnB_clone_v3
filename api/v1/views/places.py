#!/usr/bin/python3
"""
This is the Place module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State
from flasgger.utils import swag_from


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/places/get.yml', methods=['GET'])
def get_all_places(city_id):
    """List cities by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [obj.to_dict() for obj in city.places]
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/places/get_id.yml', methods=['GET'])
def get_place(place_id):
    """Get place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/places/delete.yml', methods=['DELETE'])
def del_place(place_id):
    """Delete place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/places/post.yml', methods=['POST'])
def create_obj_place(city_id):
    """Create a new instance"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    js_req = request.get_json()
    js_req['city_id'] = city_id
    user = storage.get(User, js_req['user_id'])
    if user is None:
        abort(404)
    new_obj = Place(**js_req)
    new_obj.save()
    return (jsonify(new_obj.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/places/put.yml', methods=['PUT'])
def post_place(place_id):
    """Update place by id"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    contnt = storage.get(Place, place_id)
    if contnt is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated']:
            setattr(contnt, key, value)
    storage.save()
    return jsonify(contnt.to_dict())


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/places/search.yml', methods=['POST'])
def search_places_by_id():
    """Search places by id"""
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    js_req = request.get_json()

    if js_req and len(js_req):
        states = js_req.get('states', None)
        cities = js_req.get('cities', None)
        amenities = js_req.get('amenities', None)

    if not js_req or not len(js_req) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        obj_states = [storage.get(State, s_id) for s_id in states]
        for state in obj_states:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        obj_city = [storage.get(City, c_id) for c_id in cities]
        for city in obj_city:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        obj_amenities = [storage.get(Amenity, am_id) for am_id in amenities]
        list_places = [place for place in list_places
                       if all([amenity in place.amenities
                               for amenity in obj_amenities])]

    places = []
    for place in list_places:
        place_dict = place.to_dict()
        place_dict.pop('amenities', None)
        places.append(place_dict)

    return jsonify(places)

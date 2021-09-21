#!/usr/bin/python3
"""States views"""
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<id>/places',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def view_cities_of_state(id):
    """Returns a list of all places of a city, or delete a
    place if a given id
    """
    city = storage.get(City, id)
    user = storage.get(User, id)

    if city is None or user is None:
        return abort(404)

    if request.method == 'GET':

        list = []
        for place in city.cities:
            list.append(place.to_dict())
        return jsonify(list)

    if request.method == 'POST':
        # Get the attributes from the request
        data = request.get_json()

        if isinstance(data, dict):
            pass
        else:
            return jsonify({"error": "Not a JSON"}), 400

        if 'name' not in data.keys():
            return jsonify({'error': 'Missing name'}), 400

        if 'user_id' not in data.keys():
            return jsonify({'error': 'Missing user_id'}), 400

        if 'id' in data.keys():
            data.pop("id")
        if 'created_at' in data.keys():
            data.pop("created_at")
        if 'updated_at' in data.keys():
            data.pop("updated_at")

        data.update({"place_id": id})

        # Create the object
        obj = Place(**data)

        # Save the object in storage
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/places/<id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def view_city_id(id):
    """Returns or erases a place"""
    place = storage.get(Place, id)

    if place is None:
        return abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if isinstance(data, dict):
            pass
        else:
            return jsonify({"error": "Not a JSON"}), 400

        if 'id' in data.keys():
            data.pop("id")
        if 'created_at' in data.keys():
            data.pop("created_at")
        if 'updated_at' in data.keys():
            data.pop("updated_at")

        for key, value in data.items():
            setattr(place, key, value)

        storage.save()
        return jsonify(place.to_dict())

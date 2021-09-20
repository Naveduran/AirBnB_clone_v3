#!/usr/bin/python3
"""States views"""
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/user',
                 strict_slashes=False,
                 methods=['GET', 'POST'])
def view_users():
    """Returns the list of all User objects"""
    if request.method == 'POST':

        # Get the attributes from the request
        data = request.get_json()
        if 'id' in data.keys():
            data.pop(id)
        if 'created_at' in data.keys():
            data.pop(created_at)
        if 'updated_at' in data.keys():
            data.pop(updated_at)
        if 'email' not in data.keys():
            return jsonify({'error': 'Missing email'}), 400
        if 'password' not in data.keys():
            return jsonify({'error': 'Missing password'}), 400 
        if data is None:
            return (jsonify({"error": "Not a JSON"}), 400)

        # Create the object
        obj = User(**data)

        # Save the object in storage
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201

    if request.method == 'GET':
        uaer_data = storage.all("User")
        list = []
        for name, user_obj in User.items():
            list.append(user_obj.to_dict())
        return jsonify(list)


@app_views.route('/user/<id>',
                 strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def view_user(id):
    """Returns a list of all User objects, or delete an
    object if a given id
    """
    user_data = storage.get(User, id)

    if user_data is None:
        return abort(404)

    if request.method == 'GET':
        data = user_data.to_dict()
        return jsonify(data)

    if request.method == 'DELETE':
        storage.delete(user_data)
        storage.save()
        return jsonify({})

    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return (jsonify({"error": "Not a JSON"}), 400)
        for key, value in data.items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(user_data, key, value)
        storage.save()
        user_data = user_data.to_dict()
        return jsonify(user_data)

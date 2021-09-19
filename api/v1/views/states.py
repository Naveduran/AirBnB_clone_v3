#!/usr/bin/python3
"""States views"""
from flask import jsonify, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/states', strict_slashes=False)
def view_states():
    """Returns the list of all State objects"""
    from models.state import State
    states = storage.all("State")
    list = []
    for name, state in states.items():
        list.append(state.to_dict())
    return jsonify(list)

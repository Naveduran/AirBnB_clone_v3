#!/usr/bin/python3
"""Initialize flask functions"""
from flask import jsonify, make_response
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def view_status():
    """Returns a JSON"""
    response = make_response(jsonify({"status": "OK"}))
    response.headers["Content-Type"] = "application/json"
    return response

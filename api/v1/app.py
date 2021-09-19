#!/usr/bin/python3
"""Defines flask aplications"""

from models import storage
from api.v1.views import app_views
from os import getenv


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """Close process"""
    storage.close()

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = int(getenv('HBNB_API_PORT', default=5000))
    app.run(host=host, port=port)

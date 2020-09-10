#!/usr/bin/python3
"""
Flask Index
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route("/status")
def json_status():
    """ Check the status"""
    return jsonify(status='OK')


@app_views.route("/stats")
def count_classes():
    """Retrieves the number of each objects by type."""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)

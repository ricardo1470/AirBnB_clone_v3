#!/usr/bin/python3
"""Flask Reviews"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User
from models.place import Place
from models.city import City
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""

    PlaceID = storage.get('Place', place_id)
    if PlaceID is None:
        abort(404)

    dic = []

    for PlaceID in PlaceID.reviews:
        new_dict.append(PlaceID.to_dict())
    return jsonify(dic)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""

    reviewID = storage.get('Review', review_id)

    if reviewID is None:
        abort(404)
    return jsonify(reviewID.to_dict())


@app_views.route('/reviews/<review_id>', methods=['Delete'],
                 strict_slashes=False)
def delete_review_places_by_id(review_id):
    """Deletes a Review object"""

    reviewID = storage.get('Review', review_id)

    if reviewID is None:
        abort(404)

    storage.delete(reviewID)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_a_review(place_id):
    """Creates a Review"""

    if not storage.get("Place", place_id):
        abort(404)

    json_input = request.get_json()

    if not json_input:
        abort(400, 'Not a JSON')

    if "user_id" not in json_input:
        abort(400, 'Missing user_id')

    if storage.get("User", json_input["user_id"]) is None:
        abort(404)

    if "text" not in json_input:
        abort(400, 'Missing text')

    review = Review(user_id=json_input["user_id"],
                    text=json_input["text"],
                    place_id=place_id)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_a_review_place(review_id):
    """Updates a Review object"""

    reviewID = storage.get('Review', review_id)

    if reviewID is None:
        abort(404)

    json_input = request.get_json()

    if json_input is None:
        abort(400, "Not a JSON")

    for key, value in json_input.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(reviewID, key, value)
    storage.save()
    return jsonify(reviewID.to_dict()), 200

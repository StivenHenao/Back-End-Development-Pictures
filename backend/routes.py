from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return picture
    return {"message": "picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################


@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()
    if not new_picture:
        return {"message": "Invalid input parameter"}, 422
    
    if 'id' not in new_picture:
        return {"message": "Picture ID is required"}, 422
    
    if any(pic.get('id') == new_picture.get('id') for pic in data):
        return {"Message": f"picture with id {new_picture['id']} already present"}, 302
    
    try:
        data.append(new_picture)
        return {"id": new_picture['id']}, 201
    except Exception as e:
        return {"message": str(e)}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_picture = request.get_json()

    if not updated_picture:
        return jsonify({"message": "Invalid input parameter"}), 422

    try:
        for index, picture in enumerate(data):
            if picture["id"] == id:
                updated_picture["id"] = id
                data[index] = updated_picture
                return jsonify({"message": "picture updated"}), 200

        return jsonify({"message": "imagen no encontrada"}), 404

    except NameError:
        return jsonify({"message": "data not defined"}), 500

######################################################################
# DELETE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    try:
        for picture in data:
            if picture["id"] == id:
                data.remove(picture)
                return jsonify({"message": f"Picture with ID {id} deleted"}), 204
        return jsonify({"message": "picture not found"}), 404
    except NameError:
        return jsonify({"message": "data not defined"}), 500
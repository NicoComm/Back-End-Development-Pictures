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
    urls = jsonify([item["pic_url"] for item in data])
    return urls

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((item for item in data if item["id"] == id), None)
    if picture is None:
        return {"error": "Picture not found"}, 404
    return jsonify(picture)

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = next((item for item in data if item["id"] == request.json.get("id")), None)
    if picture:
        return {"Message": f"picture with id {request.json.get('id')} already present"}, 302
        
    dict_req={
        "id": request.json.get("id"),
        "pic_url": request.json.get("pic_url"),
        "event_country": request.json.get("event_country"),
        "event_state": request.json.get("event_state"),
        "event_city": request.json.get("event_city"),
        "event_date": request.json.get("event_date"),
    }

    data.append(dict_req)
    return dict_req, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return {"message": "picture not found"}, 404
        
    data_req = request.json
    for key, value in data_req.items():
        picture[key] = value   
    return jsonify(picture)

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return {"message": "picture not found"}, 404
    
    data.remove(picture)

    return "", 204
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
    if data:
        return data, 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data: 
        for items in data:
            if items['id'] == id:
                return items,200
        return {"message": "Not found"}, 404        
    return {"message": "Internal server error"}, 500

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    if request.json:
        formatted_data = {
            'id': request.json['id'],
            'pic_url': request.json['pic_url'],
            'event_country': request.json['event_country'],
            'event_state': request.json['event_state'],
            'event_city': request.json['event_city'],
            'event_date': request.json['event_date']
        }
        for picture in data:
            if picture['id'] == formatted_data['id']:
                picture_id = picture['id']
                return {f"Message": f"picture with id {picture_id} already present"}, 302
        data.append(formatted_data)        
        return formatted_data, 201
    return {"message": "Internal server error"}, 500               

    

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    if request.json:
        formatted_data = {
            'pic_url': request.json['pic_url'],
            'event_country': request.json['event_country'],
            'event_state': request.json['event_state'],
            'event_city': request.json['event_city'],
            'event_date': request.json['event_date']
        }
        for picture in data:
            if picture['id'] == id:
                picture['pic_url'] = formatted_data['pic_url']
                picture['event_country'] = formatted_data['event_country']
                picture['event_state'] = formatted_data['event_state']
                picture['event_city'] = formatted_data['event_city']
                picture['event_date'] = formatted_data['event_date']
                return picture, 200
        return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture['id'] == id:
            data.remove(picture)
            return {},204
    return {"message": "picture not found"}, 404        

# from os import name
from flask import Blueprint, jsonify, request

from app import db
from app.models.planets import Planet

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods = ["POST"])
def create_planet():
    request_body = request.get_json()
    
    new_planet = Planet(
        name = request_body["name"],
        description = request_body["description"],
        is_colonized = request_body["is_colonized"]
    )

    db.session.add(new_planet)
    db.session.commit()
    
    return {
        "id" : new_planet.id
    }, 201
    
    

#currently unused
def id_validation(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify({"msg": f"Invalid planet ID: '{id}'"}), 400


    if id not in [planet.to_dictionary()["id"] for planet in planets]:
        return jsonify({"msg": f"Planet ID not found: '{id}'"}), 404

    return None



@planets_bp.route("", methods=["GET"])
def get_all_planets():
    return jsonify([planet.to_dictionary() for planet in planets])


@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        return jsonify({"msg": f"Invalid planet ID: '{planet_id}'"}), 400

    if planet_id not in [planet.to_dictionary()["id"] for planet in planets]:
        return jsonify({"msg": f"Planet ID not found: '{planet_id}'"}), 404


    chosen_planet = [planet.to_dictionary() for planet in planets if planet.to_dictionary()["id"]==planet_id]

    return jsonify(chosen_planet)

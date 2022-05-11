# from os import name
from flask import Blueprint, jsonify, request, abort, make_response
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
        "id" : new_planet.id,
        "msg": f"Successfully created cat with id {new_planet.id}"
    }, 201


@planets_bp.route("", methods=["GET"])
def get_all_planets():
    response = []
    planets = Planet.query.all()
    for planet in planets:
        response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "is_colonized": planet.is_colonized
            }
        )
    return jsonify(response)

def get_planet_or_abort(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {planet_id}"}
        abort(make_response(jsonify(rsp), 400))
    chosen_planet = Planet.query.get(planet_id)

    if chosen_planet is None:
        rsp = {"msg": f"Could not find planet with id {planet_id}"}
        abort(make_response(jsonify(rsp), 404))
    return chosen_planet


@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):    
    chosen_planet = get_planet_or_abort(planet_id)
    return jsonify({
                "id": chosen_planet.id,
                "name": chosen_planet.name,
                "description": chosen_planet.description,
                "is_colonized": chosen_planet.is_colonized
            }), 200
    
@planets_bp.route("/<planet_id>", methods=["PUT"])
def replace_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        return jsonify({'msg': f"Invalid planet id: '{planet_id}'. ID must be an integer"}), 400

    request_body = request.get_json()

    if "name" not in request_body or \
        "description" not in request_body or \
        "is_colonized" not in request_body:
        return jsonify({'msg': f"Request must include name, description, and is_colonized"}), 400

    chosen_planet = Planet.query.get(planet_id)
    
    if chosen_planet is None:
        return jsonify({'msg': f'Could not find car with id {planet_id}'}), 404

    chosen_planet.name = request_body["name"]
    chosen_planet.description = request_body["description"]
    chosen_planet.is_colonized = request_body["is_colonized"]

    db.session.commit()

    return make_response(
        jsonify({'msg': f"Successfully replaced car with id {planet_id}"}),
        200
    )


@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_one_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        return jsonify({'msg': f"Invalid planet id: '{planet_id}'. ID must be an integer"}), 400

    planet_id = Planet.query.get(planet_id)

    if planet_id is None:
        return jsonify({'msg': f'Could not find car with id {planet_id}'}), 404

    db.session.delete(planet_id)
    db.session.commit()

    return jsonify({'msg': f'Deleted planet with id {planet_id}'})
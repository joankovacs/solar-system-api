from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, is_colonized):
        self.id = id
        self.name = name
        self.description = description
        self.is_colonized = is_colonized
        
    def to_dictionary(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_colonized": self.is_colonized,    
        }    
        
planets = [
    Planet(0, "Artemis", "Hot rocky world with lots of metal ores", False),
    Planet(1, "Calypso", "Shattered remnants of world that once had life", False),
    Planet(2, "Veridia", "Once a center of civilization, now a runaway greenhouse jungle", True),
    Planet(3, "Azure Spire", "Capital of The Galactic Imperium", True),
    Planet(4, "Aura", "Gas giant with 100 moons", True)
]

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

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


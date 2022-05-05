from app import db

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    is_colonized = db.Column(db.String)


# class Planet:
#     def __init__(self, id, name, description, is_colonized):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.is_colonized = is_colonized
        
#     def to_dictionary(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "description": self.description,
#             "is_colonized": self.is_colonized,    
#         }    
        
# planets = [
#     Planet(0, "Artemis", "Hot rocky world with lots of metal ores", False),
#     Planet(1, "Calypso", "Shattered remnants of world that once had life", False),
#     Planet(2, "Veridia", "Once a center of civilization, now a runaway greenhouse jungle", True),
#     Planet(3, "Azure Spire", "Capital of The Galactic Imperium", True),
#     Planet(4, "Aura", "Gas giant with 100 moons", True)
# ]

import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.planets import Planet

@pytest.fixture
def app():
    app = create_app({"TESTING" : True})
    
    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()
        
    with app.app_context():
        db.create_all() #setup our db
        yield app #like return statement. return our app for our test to use
        
    with app.app_context():
        db.drop_all() #then this will clean up everything we use in our datebase. 
        #To start over with a clean database
        
@pytest.fixture
def client(app): #pytest fixture will do it for me. same spelling and case
    return app.test_client()

@pytest.fixture
def four_planets(app):
    artemis= Planet(id = 1, name = "Artemis", description = "Hot rocky world with lots of metal ores", is_colonized = "False")
    calypso = Planet(id = 2, name = "Calypso", description = "Shattered remnants of world that once had life", is_colonized = "False")
    veridia = Planet(id = 3, name = "Veridia", description = "Once a center of civilization, now a runaway greenhouse jungle", is_colonized = "True")
    azure_spire = Planet(id = 4, name = "Azure Spire", description = "Capital of The Galactic Imperium", is_colonized = "True")

    db.session.add(artemis)
    db.session.add(calypso)
    db.session.add(veridia)
    db.session.add(azure_spire)
 
    
    db.session.commit()



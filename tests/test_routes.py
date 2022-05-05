from tests.conftest import four_planets
from app.models.planets import Planet

def test_get_all_planets_with_empty_db_returns_empty_list(client):
    response = client.get('/planets')
    response_body = response.get_json()
    
    assert response.status_code == 200
    assert response_body == []
    
def test_get_one_planet_with_populated_db_returns_planet_json(client, four_planets):
    response = client.get('/planets/1')
    response_body = response.get_json()
    
    assert response.status_code == 200
    assert response_body == {
        "id" : 1,
        "name" : "Artemis",
        "description" : "Hot rocky world with lots of metal ores",
        "is_colonized" : "False"
    }
    
def test_get_all_planets_with_populated_db_returns_populated_list(client, four_planets):
    response = client.get('/planets')
    response_body = response.get_json()
    
    assert response.status_code == 200
    assert len(response_body) == 4
    
    
def test_post_one_planet_creates_planet_in_db(client):
    response = client.post('/planets', json = {"name" : "Aura", "description" : "Gas giant with 100 moons", "is_colonized" : "True"})
    response_body = response.get_json()
    assert response.status_code == 201
    assert "id" in response_body
    assert "msg" in response_body
    
    planets = Planet.query.all()
    assert len(planets) == 1
    assert planets[0].name == "Aura"
    assert planets[0].description == "Gas giant with 100 moons"
    assert planets[0].is_colonized == "True"
    
def test_get_one_planet_with_empty_db_returns_404(client):
    response = client.get('/planets/6')
    assert response.status_code == 404
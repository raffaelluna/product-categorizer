#tests will run the fixtures that are declared here
import pytest

from api.app import create_app
from api.config import TestingConfig

#fixtures are functions that runs before the tests and are used
#as arguments for the tests
#https://flask.palletsprojects.com/en/1.1.x/testing/
@pytest.fixture
def app():
    app = create_app(config_object=TestingConfig)
    
    #https://diegoquintanav.github.io/flask-contexts.html
    with app.app_context():
        yield app
 
@pytest.fixture       
def api_test_client(app):
    with app.test_client() as test_client:
        yield test_client
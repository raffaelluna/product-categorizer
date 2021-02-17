from flask import Flask

def create_app(config_object):
    
    flask_app = Flask('categorizer_api')
    
    #SWITCH BETWEEN TESTING, DEVELOPMENT AND PRODUCTION ENVIRONMENTS
    flask_app.config.from_object(config_object)
    
    from api.controller import categorizer_app
    flask_app.register_blueprint(categorizer_app)
    
    return flask_app
import pickle

from flask import Blueprint, request, jsonify
from processing.preprocessors import ProductCategorizer

#LOAD MODELS
categorizer = ProductCategorizer()

#CREATE A BLUEPRINT TO ENSURE MODULARITY
#https://flask.palletsprojects.com/en/1.1.x/blueprints/
categorizer_app = Blueprint('categorizer_app', __name__)

@categorizer_app.route('/health', methods=['GET'])
def health():
    if request.method == 'GET':
        return 'ok'
    
@categorizer_app.route('/v1/predict', methods=['POST'])
def predict():
    return    

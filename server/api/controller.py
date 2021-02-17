import pandas as pd

from flask import Blueprint, request, jsonify
from processing.preprocessors import ProductCategorizer
from config.config import FEATURES_TO_DROP, FEATURES_TO_NORMALIZE
#from api.validation import validate_input

#LOAD MODELS
categorizer = ProductCategorizer()

#CREATE A BLUEPRINT TO ENSURE MODULARITY
#https://flask.palletsprojects.com/en/1.1.x/blueprints/
categorizer_app = Blueprint('categorizer_app', __name__)

@categorizer_app.route('/health', methods=['GET'])
def health():
    if request.method == 'GET':
        return 'ok', 200
    
@categorizer_app.route('/v1/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        
        #GET JSON DATA
        received_json = request.get_json()
        
        #VALIDATE INPUT
        #validated_data, errors = validate_input(received_json)
        #if errors != None:
        #    return 'There are errors in input data, please check.', 400
        data = pd.DataFrame(received_json)
        input_data, _ = categorizer.data_transformer(data, 
                                                     FEATURES_TO_DROP, 
                                                     FEATURES_TO_NORMALIZE)
        
        pred = categorizer.predict(input_data)
        response = {"categories": pred.tolist()}
    
        
        return jsonify(response), 200   

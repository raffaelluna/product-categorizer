import os
import pandas as pd
import sys
sys.path.append('../')

import dotenv
dotenv.load_dotenv()

from flask import Blueprint, request, jsonify

from processing.preprocessors import ProductCategorizer
from config.config import FEATURES_TO_DROP, FEATURES_TO_NORMALIZE
from config.logger import ApiLogger
from api.validation import validate_input


#LOAD MODELS
categorizer = ProductCategorizer()
logger = ApiLogger()


LOGS_PATH = os.getenv("LOGS_PATH")


#CREATE A BLUEPRINT TO ENSURE MODULARITY
#https://flask.palletsprojects.com/en/1.1.x/blueprints/
categorizer_app = Blueprint('categorizer_app', __name__)


@categorizer_app.route('/health', methods=['GET'])
def health():
    if request.method == 'GET':
        return 'ok', 200
    
@categorizer_app.route('/v1/categorize', methods=['POST'])
def predict():
    if request.method == 'POST':
        
        #GET JSON DATA
        received_json = request.get_json()
        
        if received_json is not None:
            #VALIDATE INPUT
            validated_data, errors = validate_input(received_json)
            
            if errors is not None:
                logger.log_api(file=LOGS_PATH, message="JSON received with errors!")
                return f'There are errors in input data, please check. Error: {errors}', 400
        else:
            logger.log_api(file=LOGS_PATH, message="No JSON received!")
            return 'No JSON file received, please check.', 400
        
        logger.log_api(file=LOGS_PATH, message="JSON received with no errors!")
        
        data = pd.DataFrame(validated_data)
        
        input_data, _ = categorizer.data_transformer(data, 
                                                     FEATURES_TO_DROP, 
                                                     FEATURES_TO_NORMALIZE)
        
        pred = categorizer.predict(input_data)
        response = {"categories": pred.tolist()}
    
        
        return jsonify(response), 200   

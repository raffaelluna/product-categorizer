###VERIFICAR SE O ENDPOINT HEALTH (GET) RETORNA 200 - ok
###VERIFICAR SE O ENDPOINT V1/CATEGORIZE RETORNA 200 QUANDO RECEBE JSON VALIDO - ok
###VERIFICAR SE O ENDPOINT V1/CATEGORIZE RETORNA 400 QUANDO RECEBE JSON INVALIDO - ok
###VERIFICAR SE A PREDIÇÃO COM JSON VALIDO RETORN UMA LISTA COM TAMANHO 500 - ok
###UM ASSERT POR TEST
import os
import json

import dotenv
dotenv.load_dotenv()

VALID_JSON_PATH = os.getenv("TEST_PRODUCTS_PATH")
INVALID_JSON_PATH = os.getenv("INVALID_TEST_PRODUCTS_PATH")

def test_health_point(api_test_client):
    response = api_test_client.get('/health')
    assert response.status_code == 200
    
def test_valid_prediction_returns_200(api_test_client):
    
    with open(VALID_JSON_PATH, "rb") as f:
        valid_json = json.load(f)
    
    response = api_test_client.post('v1/categorize', json=valid_json)
    
    assert response.status_code == 200
    
def test_valid_prediction_returns_len_500(api_test_client):
    
    with open(VALID_JSON_PATH, "rb") as f:
        valid_json = json.load(f)
        
    response = api_test_client.post('v1/categorize', json=valid_json)
    response_json = json.loads(response.data)
    prediction = response_json['categories']
    
    assert len(prediction) == 500

def test_invalid_json_returns_400(api_test_client):
    
    with open(INVALID_JSON_PATH, "rb") as f:
        invalid_json = json.load(f)
        
    response = api_test_client.post('v1/categorize', json=invalid_json)
    
    assert response.status_code == 400
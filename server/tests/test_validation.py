###VERIFICAR SE JSON VALIDO NÃO RETORNA ERRO - ok
###VERIFICAR SE JSON INVALIDO RETORNA ERRO - ok
import os
import json

import dotenv
dotenv.load_dotenv()

from api.validation import validate_input

VALID_JSON_PATH = os.getenv("TEST_PRODUCTS_PATH")
INVALID_JSON_PATH = os.getenv("INVALID_TEST_PRODUCTS_PATH")

def test_valid_input_returns_no_error():
    
    with open(VALID_JSON_PATH, "rb") as f:
        data = json.load(f)
        
    _, errors = validate_input(data)
    
    assert errors == None
    
def test_invalid_input_returns_error():
    
    with open(INVALID_JSON_PATH, "rb") as f:
        data = json.load(f)
        
    _, errors = validate_input(data)
    
    assert errors == {0: {'product_id': ['Field may not be null.']}}
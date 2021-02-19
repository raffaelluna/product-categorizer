###VERIFICAR SE O METODO text_normalizer FUNCIONA CORRETAMENTE - ok
###VERIFICAR SE O METODO data_transformer FUNCIONA CORRETAMENTE
import pandas as pd

from processing.preprocessors import ProductCategorizer
from config.config import FEATURES_TO_DROP, FEATURES_TO_NORMALIZE

from sklearn.feature_extraction.text import CountVectorizer


RAW_TEXT = """TÉxto p/ tEstaR se dE da Do Ó cAtègôriZAdor estÁ fÚúnCIOnanDõ!@#"""
PROCESSED_TEXT = """texto p testar categorizador fuuncionando"""

RAW_JSON = {"product_id":14180109,
            "seller_id":3191400,
            "query":"prateleira",
            "search_page":1,
            "position":32,
            "title":"Trio de Nichos Prateleira",
            "concatenated_tags":"prateleiras decoracao gaveteiros nichos prateleiras nichos",
            "creation_date":"2017-08-23 22:17:01",
            "price":97.060005,
            "weight":7492.0,
            "express_delivery":1,
            "minimum_quantity":1,
            "view_counts":729,
            "order_counts":32.0,
            "category":"Decoração"}

PROCESSED_JSON = {"title":"trio nichos prateleira",
                  "query_tags":"prateleira prateleiras decoracao gaveteiros nichos prateleiras nichos"}

categorizer = ProductCategorizer()

def test_text_preprocessor():
    
    test_text = categorizer.text_normalizer(RAW_TEXT)
    
    assert test_text == PROCESSED_TEXT
    
#def test_data_transformer():
#    
#    data_to_check = pd.DataFrame(RAW_JSON, index=[0])
#    processed_data = categorizer.data_transformer(data_to_check, FEATURES_TO_DROP, FEATURES_TO_NORMALIZE)
#    
#    true_data = pd.DataFrame(PROCESSED_JSON, index=[0])
#    X_tfidf = categorizer.data_transformer(true_data, FEATURES_TO_DROP, FEATURES_TO_NORMALIZE, first_steps=False)
#    print(X_tfidf)
#    
#    assert X_tfidf == processed_data
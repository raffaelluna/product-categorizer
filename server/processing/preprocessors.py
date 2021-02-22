import os
import pickle
import unicodedata
import re
import pandas as pd

import sys
sys.path.append('../')

from config.logger import ProcessorLogger
from sklearn.feature_extraction.text import CountVectorizer
from stop_words import get_stop_words

#import nltk
#nltk.download('rslp')

import dotenv
dotenv.load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH")
LOGS_PATH = os.getenv("LOGS_PATH")


logger = ProcessorLogger()

class ProductCategorizer:
    
    def __init__(self):
        
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        
        self.fitted_model = model['Model']
        self.cv = model['Count Vectorizer']
        self.tfidf = model['TF-IDF']
        self.labelencoder = model['Label Encoder']
        
        #portuguese stemmer
        #self.stemmer = nltk.stem.RSLPStemmer()
    
    @staticmethod
    def accents_remover(text):
        #https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        return str(text)
    
    @staticmethod
    def special_char_remover(text):
        return re.sub('[^A-Za-z0-9 ]+', '', text)
    
    @staticmethod
    def text_to_lowercase(text):    
        return str.lower(text)
    
    @staticmethod
    def stop_words_remover(text, language='portuguese'):
        text = ' '.join([word for word in text.split() if word not in (get_stop_words(language))])
        return text
    
    def text_stemmer(self, text):
        words_list = [self.stemmer.stem(word) for word in text.split()]
        return ' '.join(words_list)
    
    def text_normalizer(self, text, stem=True):
        
        try:
            text = self.text_to_lowercase(text)
            text = self.accents_remover(text)
            text = self.special_char_remover(text)
            text = self.stop_words_remover(text)
            
            #if stem:
            #    text = self.text_stemmer(text)

            return text
        
        except Exception as e:
            logger.log_processor(file=LOGS_PATH, message=f"An exception occured in text_normalizer method! Exception: {e}")
            raise Exception()
        
    def data_transformer(self, df, features_to_drop, features_to_normalize):
        
        try:
            X = df.copy()
            X = X.drop(labels=features_to_drop, axis=1)
            X = X.dropna(axis=0).reset_index(drop=True)

            for feature in features_to_normalize:
                X[feature] = X[feature].apply(lambda x: self.text_normalizer(x, stem=False))

            logger.log_processor(file=LOGS_PATH, message="Text normalized!")

            X.loc[:,'query_tags'] = X['query'] + str(' ') + X['concatenated_tags']
            X = X.drop(labels=['query', 'concatenated_tags'], axis=1)

            y = X['category']
            X = X[['title', 'query_tags']]
            
            cv_ = CountVectorizer(vocabulary=self.cv.get_feature_names())
            X_counts = cv_.fit_transform(X.title, X.query_tags)
            X_tfidf = self.tfidf.transform(X_counts)

            logger.log_processor(file=LOGS_PATH, message="All transformations done!")

            return X_tfidf, y
        
        except Exception as e:
            logger.log_processor(file=LOGS_PATH, message=f"An exception occured in data_transformer method! Exception: {e}")
            raise Exception()
    
    def predict(self, X):
        
        try:
            self.pred = self.fitted_model.predict(X)
            return self.labelencoder.inverse_transform(self.pred)
        
        except Exception as e:
            logger.log_processor(file=LOGS_PATH, message=f"An exception occured while predicting! Exception: {e}")
            raise Exception()
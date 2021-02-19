import os
import pickle
import unicodedata
import re
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from stop_words import get_stop_words

#import nltk
#nltk.download('rslp')

import dotenv
dotenv.load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH")


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
        
        text = self.text_to_lowercase(text)
        text = self.accents_remover(text)
        text = self.special_char_remover(text)
        text = self.stop_words_remover(text)
        
        #if stem:
        #    text = self.text_stemmer(text)
            
        return text
    
    def data_transformer(self, df, features_to_drop, features_to_normalize):
        
        X = df.copy()
        X = X.drop(labels=features_to_drop, axis=1)
        X = X.dropna(axis=0).reset_index(drop=True)

        for feature in features_to_normalize:
            X[feature] = X[feature].apply(lambda x: self.text_normalizer(x, stem=False))

        X.loc[:,'query_tags'] = X['query'] + str(' ') + X['concatenated_tags']
        X = X.drop(labels=['query', 'concatenated_tags'], axis=1)

        y = X['category']
        X = X[['title', 'query_tags']]
        
        cv_ = CountVectorizer(vocabulary=self.cv.get_feature_names())
        X_counts = cv_.fit_transform(X.title, X.query_tags)
        X_tfidf = self.tfidf.transform(X_counts)

        return X_tfidf, y
    
    def predict(self, X):
        self.pred = self.fitted_model.predict(X)
        return self.labelencoder.inverse_transform(self.pred)
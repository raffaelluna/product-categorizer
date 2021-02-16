import pandas as pd
from sklearn.model_selection import train_test_split

from config.config import SEED

def load_data(path):
    return pd.read_csv(path)

def split_data(X, y, test_size=0.2, seed=SEED):
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
    
    return X_train, X_test, y_train, y_test
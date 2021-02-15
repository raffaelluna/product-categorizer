import pandas as pd

def load_data(path):
    return pd.read_csv(path)

def split_data(df):
    return
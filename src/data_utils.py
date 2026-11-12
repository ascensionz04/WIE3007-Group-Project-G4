import pandas as pd
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42
TEST_SIZE = 0.2


def load_data(path="data/processed/dataset.csv"):
    return pd.read_csv(path)


def split_data(df, target):
    """Shared split so every model is trained and tested on the same rows."""
    X = df.drop(columns=[target])
    y = df[target]
    return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y)

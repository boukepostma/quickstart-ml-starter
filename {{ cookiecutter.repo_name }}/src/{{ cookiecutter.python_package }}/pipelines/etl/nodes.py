import pandas as pd


def extract_transform_load(df: pd.DataFrame, label_column: str)->pd.DataFrame:
    features = df.drop(columns=[label_column])
    labels = df[[label_column]]
    return features, labels

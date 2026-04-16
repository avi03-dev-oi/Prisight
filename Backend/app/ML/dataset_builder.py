import numpy as np

def create_lstm_dataset(df, feature_cols, target_col, window_size=7):
    X, y = [], []

    for i in range(len(df) - window_size):
        X.append(df[feature_cols].iloc[i:i+window_size].values)
        y.append(df[target_col].iloc[i+window_size])

    return np.array(X), np.array(y)

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


def preprocess_data(df, features):
    X = df[features].copy()

    for col in X.select_dtypes(include=['object']).columns:
        X[col] = X[col].astype(str)

    num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = X.select_dtypes(include=['object']).columns.tolist()

    numeric_transformer = Pipeline(steps=[
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, num_cols),
            ("cat", categorical_transformer, cat_cols),
        ]
    )

    return preprocessor.fit_transform(X)

def treat_outliers(
    df: pd.DataFrame,
    cols: list,
    method: str = "iqr",          # "iqr" ou "zscore"
    strategy: str = "winsorize",  # "winsorize" (cap/clip) ou "remove"
    factor: float = 1.5,          # multiplicador do IQR (1.5 padrão)
    z: float = 4.0,               # limiar de z-score se method="zscore"
    return_info: bool = True
):

    df_out = df.copy()
    info = {"limits": {}, "n_capped": {}, "n_removed": 0}

    # Calcula limites por coluna
    limits = {}
    for c in cols:
        s = df_out[c].astype(float)
        if method == "iqr":
            q1, q3 = s.quantile(0.25), s.quantile(0.75)
            iqr = q3 - q1
            low, high = q1 - factor * iqr, q3 + factor * iqr
        elif method == "zscore":
            mu, sd = s.mean(), s.std(ddof=0)
            low, high = mu - z * sd, mu + z * sd
        else:
            raise ValueError("method deve ser 'iqr' ou 'zscore'")
        limits[c] = (low, high)

    if strategy == "remove":

        mask = np.ones(len(df_out), dtype=bool)
        for c, (low, high) in limits.items():
            mask &= df_out[c].between(low, high) | df_out[c].isna()
        info["n_removed"] = int((~mask).sum())
        df_out = df_out[mask].reset_index(drop=True)
    elif strategy == "winsorize":
        # Faz clip por coluna
        for c, (low, high) in limits.items():
            before = df_out[c].copy()
            df_out[c] = df_out[c].clip(lower=low, upper=high)
            info["n_capped"][c] = int((before != df_out[c]).sum())
    else:
        raise ValueError("strategy deve ser 'winsorize' ou 'remove'")

    if return_info:
        info["limits"] = limits
        return df_out, info
    return df_out
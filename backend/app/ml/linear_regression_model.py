from sklearn.linear_model import LinearRegression

from sklearn.metrics import r2_score

from sklearn.model_selection import train_test_split

import pandas as pd

import joblib


def train_linear_regression(df):

    df = df.copy()

    # CLEAN DATA

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["sales"] = pd.to_numeric(
        df["sales"],
        errors="coerce"
    )

    df = df.dropna()

    # DATE FEATURES

    df["day"] = df["date"].dt.day

    df["month"] = df["date"].dt.month

    df["year"] = df["date"].dt.year

    # FEATURES

    X = df[[
        "day",
        "month",
        "year"
    ]]

    y = df["sales"]

    # TRAIN TEST SPLIT

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # MODEL

    model = LinearRegression()

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(X_test)

    accuracy = r2_score(
        y_test,
        predictions
    ) * 100

    # SAVE MODEL

  #  joblib.dump(
   #     model,
    #    "app/ml/saved_linear_regression_model.pkl"
   # )

    return round(accuracy, 2)
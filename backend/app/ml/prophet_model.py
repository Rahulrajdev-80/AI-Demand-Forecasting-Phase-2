from prophet import Prophet
from sklearn.metrics import r2_score
import pandas as pd


def train_prophet(df):

    df = df.copy()

    # Detect date column
    possible_date_cols = [
        "date",
        "order_date",
        "Order Date"
    ]

    date_col = None

    for col in possible_date_cols:
        if col in df.columns:
            date_col = col
            break

    if not date_col:
        raise Exception("No date column found")

    # Detect sales column
    possible_sales_cols = [
        "sales",
        "Sales"
    ]

    sales_col = None

    for col in possible_sales_cols:
        if col in df.columns:
            sales_col = col
            break

    if not sales_col:
        raise Exception("No sales column found")

    # Create dataframe for Prophet
    prophet_df = pd.DataFrame()

    prophet_df["ds"] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

    prophet_df["y"] = pd.to_numeric(
        df[sales_col],
        errors="coerce"
    )

    # Remove invalid rows
    prophet_df = prophet_df.dropna()

    # Reset index
    prophet_df = prophet_df.reset_index(drop=True)

    # Train model
    model = Prophet()

    model.fit(prophet_df)

    # Predict SAME rows only
    forecast = model.predict(
        prophet_df[["ds"]]
    )

    predictions = forecast["yhat"]

    # Calculate accuracy
    accuracy = r2_score(
        prophet_df["y"],
        predictions
    ) * 100

    return round(accuracy, 2)
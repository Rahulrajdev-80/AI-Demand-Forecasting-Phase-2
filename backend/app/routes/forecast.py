from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from prophet import Prophet

import pandas as pd

from app.database.session import SessionLocal

from app.services.forecast_service import (
    get_models,
    generate_forecast
)

from app.ml.prophet_model import train_prophet

from app.ml.linear_regression_model import (
    train_linear_regression
)

from app.ml.random_forest_model import (
    train_random_forest
)

from app.models.dataset_model import Dataset

from app.models.forecast_model import (
    ForecastHistory
)

from app.utils.jwt_handler import verify_token


router = APIRouter(
    prefix="/api/forecast",
    tags=["Forecasting"]
)


# DATABASE CONNECTION

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# GET AVAILABLE MODELS

@router.get("/models")
def forecast_models():

    return {
        "models": get_models()
    }


# GENERATE FORECAST

@router.post("/{dataset_id}")
def create_forecast(
    dataset_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    result = generate_forecast(
        db,
        dataset_id
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    return {
        "message": "Forecast generated",
        "forecast": result
    }


# COMPARE AI MODELS

@router.get("/{dataset_id}/compare")
def compare_models_api(
    dataset_id: int,
    db: Session = Depends(get_db)
):

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    # READ CSV

    df = pd.read_csv(dataset.file_path)

    # POSSIBLE COLUMN NAMES

    possible_date_cols = [
        "date",
        "Date",
        "order_date",
        "Order Date"
    ]

    possible_sales_cols = [
        "sales",
        "Sales",
        "amount",
        "Amount"
    ]

    date_col = None
    sales_col = None

    # FIND DATE COLUMN

    for col in possible_date_cols:

        if col in df.columns:
            date_col = col
            break

    # FIND SALES COLUMN

    for col in possible_sales_cols:

        if col in df.columns:
            sales_col = col
            break

    # VALIDATION

    if not date_col or not sales_col:

        raise HTTPException(
            status_code=400,
            detail="Required columns not found"
        )

    # CLEAN DATA

    cleaned_df = pd.DataFrame()

    cleaned_df["date"] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

    cleaned_df["sales"] = pd.to_numeric(
        df[sales_col],
        errors="coerce"
    )

    cleaned_df = cleaned_df.dropna()

    # TRAIN MODELS

    prophet_accuracy = train_prophet(
        cleaned_df
    )

    linear_accuracy = train_linear_regression(
        cleaned_df
    )

    random_accuracy = train_random_forest(
        cleaned_df
    )

    return {
        "dataset_id": dataset_id,
        "models": [
            {
                "name": "Prophet",
                "accuracy": prophet_accuracy
            },
            {
                "name": "Linear Regression",
                "accuracy": linear_accuracy
            },
            {
                "name": "Random Forest",
                "accuracy": random_accuracy
            }
        ]
    }


# FORECAST GRAPH DATA

@router.get("/{dataset_id}/graph")
def forecast_graph(
    dataset_id: int,
    db: Session = Depends(get_db)
):

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    df = pd.read_csv(dataset.file_path)

    possible_date_cols = [
        "date",
        "Date",
        "order_date",
        "Order Date"
    ]

    possible_sales_cols = [
        "sales",
        "Sales",
        "amount",
        "Amount"
    ]

    date_col = None
    sales_col = None

    for col in possible_date_cols:

        if col in df.columns:
            date_col = col
            break

    for col in possible_sales_cols:

        if col in df.columns:
            sales_col = col
            break

    if not date_col or not sales_col:

        raise HTTPException(
            status_code=400,
            detail="Required columns not found"
        )

    cleaned_df = pd.DataFrame()

    cleaned_df["date"] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

    cleaned_df["sales"] = pd.to_numeric(
        df[sales_col],
        errors="coerce"
    )

    cleaned_df = cleaned_df.dropna()

    return {
        "dates": cleaned_df["date"].astype(str).tolist(),
        "sales": cleaned_df["sales"].tolist()
    }


# FUTURE 30 DAYS FORECAST

@router.get("/{dataset_id}/future")
def future_forecast(
    dataset_id: int,
    db: Session = Depends(get_db)
):

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    df = pd.read_csv(dataset.file_path)

    possible_date_cols = [
        "date",
        "Date",
        "order_date",
        "Order Date"
    ]

    possible_sales_cols = [
        "sales",
        "Sales",
        "amount",
        "Amount"
    ]

    date_col = None
    sales_col = None

    for col in possible_date_cols:

        if col in df.columns:
            date_col = col
            break

    for col in possible_sales_cols:

        if col in df.columns:
            sales_col = col
            break

    if not date_col or not sales_col:

        raise HTTPException(
            status_code=400,
            detail="Required columns not found"
        )

    prophet_df = pd.DataFrame()

    prophet_df["ds"] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

    prophet_df["y"] = pd.to_numeric(
        df[sales_col],
        errors="coerce"
    )

    prophet_df = prophet_df.dropna()

    model = Prophet()

    model.fit(prophet_df)

    future = model.make_future_dataframe(
        periods=30
    )

    forecast = model.predict(future)

    result = forecast[
        ["ds", "yhat"]
    ].tail(30)

    return {
        "forecast": result.to_dict(
            orient="records"
        )
    }


# FORECAST HISTORY

@router.get("/{dataset_id}/history")
def forecast_history(
    dataset_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    history = db.query(
        ForecastHistory
    ).filter(
        ForecastHistory.dataset_id == dataset_id
    ).all()

    return history
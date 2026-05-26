import pandas as pd

from sqlalchemy.orm import Session

from app.models.dataset_model import Dataset
from app.models.activity_model import Activity


def dashboard_analytics(
    db: Session,
    dataset_id: int
):

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:
        return None

    file_path = dataset.filepath

    df = pd.read_csv(
        file_path,
        encoding="latin1"
    )

    # Total Sales

    total_sales = round(
        df["Sales"].sum(),
        2
    )

    # Total Orders

    total_orders = len(df)

    # Top Products

    top_products = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .to_dict()
    )

    # Monthly Sales

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    monthly_sales = (
        df.groupby(
            df["Order Date"].dt.strftime("%Y-%m")
        )["Sales"]
        .sum()
        .to_dict()
    )

    return {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "forecast_accuracy": 92.5,
        "top_products": top_products,
        "monthly_sales": monthly_sales
    }


def recent_activities(db: Session):

    activities = db.query(Activity).all()

    return activities
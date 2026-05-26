from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.database.session import SessionLocal

from app.models.user_model import User
from app.models.dataset_model import Dataset
from app.models.forecast_model import ForecastHistory

from app.utils.jwt_handler import verify_token

from app.utils.admin_handler import verify_admin

from app.schemas.admin_schema import AdminSummarySchema


router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get(
    "/summary",
    response_model=AdminSummarySchema
)
def admin_summary(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    verify_admin(email, db)

    total_users = db.query(User).count()

    total_datasets = db.query(Dataset).count()

    total_forecasts = db.query(
        ForecastHistory
    ).count()

    return {
        "total_users": total_users,
        "total_datasets": total_datasets,
        "total_forecasts": total_forecasts
    }


@router.get("/users")
def get_users(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users


@router.get("/datasets")
def get_datasets(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    datasets = db.query(Dataset).all()

    return datasets
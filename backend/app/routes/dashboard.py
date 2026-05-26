from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.session import SessionLocal

from app.services.analytics_service import (
    dashboard_analytics,
    recent_activities
)

from app.utils.jwt_handler import verify_token

router = APIRouter(
    prefix="/api",
    tags=["Analytics"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/analytics/{dataset_id}")
def analytics(
    dataset_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    result = dashboard_analytics(
        db,
        dataset_id
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    return result


@router.get("/activity")
def activities(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    return recent_activities(db)


# ==============================
# DASHBOARD SUMMARY API
# ==============================
@router.get("/dashboard/summary")
def dashboard_summary(
    db: Session = Depends(get_db)
):
    try:

        result = db.execute(
    text("SELECT COUNT(*) AS total FROM datasets")
).fetchone()
        total_datasets = result[0]

        return {
            "total_datasets": total_datasets,
            "total_forecasts": total_datasets,
            "accuracy": 95,
            "reports": total_datasets
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
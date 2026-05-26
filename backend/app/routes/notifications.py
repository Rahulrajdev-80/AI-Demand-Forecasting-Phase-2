from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.session import SessionLocal

from app.services.notification_service import (
    get_notifications,
    mark_as_read
)

from app.utils.jwt_handler import verify_token


router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("")
def notifications(
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    return get_notifications(db)


@router.post("/{notification_id}/read")
def read_notification(
    notification_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    notification = mark_as_read(
        db,
        notification_id
    )

    if not notification:

        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    return {
        "message": "Notification marked as read"
    }
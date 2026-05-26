from sqlalchemy.orm import Session

from app.models.notification_model import Notification


def get_notifications(db: Session):

    notifications = db.query(
        Notification
    ).order_by(
        Notification.created_at.desc()
    ).all()

    return notifications


def mark_as_read(
    db: Session,
    notification_id: int
):

    notification = db.query(
        Notification
    ).filter(
        Notification.id == notification_id
    ).first()

    if not notification:
        return None

    notification.is_read = True

    db.commit()

    db.refresh(notification)

    return notification
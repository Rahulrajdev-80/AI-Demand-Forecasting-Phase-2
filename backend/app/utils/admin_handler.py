from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.user_model import User


def verify_admin(
    email: str,
    db: Session
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user or user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user
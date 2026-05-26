from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)

from datetime import datetime

from app.database.base import Base


class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)

    message = Column(String(255))

    is_read = Column(
        Boolean,
        default=False
    )

    created_at = Column(
    DateTime,
    default=datetime.utcnow,
    index=True
)
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.base import Base

class Dataset(Base):

    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255))

    file_path = Column(String(255))

    filepath = Column(String(500))
    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)

from datetime import datetime

from app.database.base import Base

class ForecastHistory(Base):

    __tablename__ = "forecast_history"

    id = Column(Integer, primary_key=True)

    dataset_id = Column(
    Integer,
    index=True
)

    model_name = Column(String(100))

    accuracy = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
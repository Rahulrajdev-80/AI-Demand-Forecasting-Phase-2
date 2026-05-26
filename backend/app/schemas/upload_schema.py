from pydantic import BaseModel
from datetime import datetime

class DatasetOut(BaseModel):

    id: int
    filename: str
    filepath: str
    uploaded_at: datetime

    class Config:
        from_attributes = True
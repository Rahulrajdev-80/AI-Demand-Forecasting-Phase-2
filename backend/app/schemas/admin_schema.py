from pydantic import BaseModel


class AdminSummarySchema(BaseModel):

    total_users: int

    total_datasets: int

    total_forecasts: int
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse

from app.database.connection import engine
from app.database.base import Base

from app.models.user_model import User

from app.routes.auth import router as auth_router

from app.models.dataset_model import Dataset

from app.models.activity_model import Activity

from app.models.forecast_model import ForecastHistory

from app.models.notification_model import Notification

from app.routes.forecast import router as forecast_router
from app.routes.notifications import router as notification_router
from app.routes.dashboard import router as dashboard_router
from app.routes.report import router as report_router

from app.routes.upload import router as upload_router

from app.routes.admin import router as admin_router
from app.routes.system import router as system_router

from fastapi.middleware.cors import CORSMiddleware

from app.middleware.error_handler import (
    global_exception_handler
)

import pandas as pd
import io

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Advanced AI Demand Forecasting Enterprise API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)

app.include_router(upload_router)

app.include_router(forecast_router)

app.include_router(dashboard_router)

app.include_router(report_router)

app.include_router(notification_router)

app.include_router(admin_router)

app.include_router(system_router)

app.add_exception_handler(
    Exception,
    global_exception_handler
)


# ================================
# NEW DATASET UPLOAD API
# ================================

@app.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    dataset_name: str = Form(...)
):
    try:

        contents = await file.read()

        df = pd.read_csv(
            io.BytesIO(contents),
            encoding='latin1'
        )

        analysis = {
            "success": True,
            "message": "Upload Successful",
            "dataset_name": dataset_name,
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "missing_values": int(df.isnull().sum().sum()),
            "column_names": list(df.columns),
            "sample_data": df.head(5).to_dict(orient="records")
        }

        return JSONResponse(
            status_code=200,
            content=analysis
        )

    except Exception as e:

        print("UPLOAD ERROR:", str(e))

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": str(e)
            }
        )


@app.get("/")
def home():
    return {
        "message": "AI Demand Forecasting Backend Running"
    }
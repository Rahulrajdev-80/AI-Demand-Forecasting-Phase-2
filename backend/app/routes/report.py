from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.database.session import SessionLocal

from app.services.report_service import (
    report_summary
)

from app.models.dataset_model import Dataset

from app.utils.jwt_handler import verify_token

import pandas as pd

from reportlab.pdfgen import canvas


router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/{dataset_id}/summary")
def get_summary(
    dataset_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    result = report_summary(
        db,
        dataset_id
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    return result


@router.get("/{dataset_id}/excel")
def export_excel(
    dataset_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    df = pd.read_csv(
        dataset.filepath,
        encoding="latin1"
    )

    output_file = "sales_report.xlsx"

    df.to_excel(
        output_file,
        index=False
    )

    return FileResponse(
        output_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="sales_report.xlsx"
    )


@router.get("/{dataset_id}/pdf")
def export_pdf(
    dataset_id: int,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:

        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    df = pd.read_csv(
        dataset.filepath,
        encoding="latin1"
    )

    pdf_file = "sales_report.pdf"

    c = canvas.Canvas(pdf_file)

    c.drawString(
        100,
        800,
        "AI Demand Forecasting Report"
    )

    c.drawString(
        100,
        760,
        f"Total Sales: {df['Sales'].sum()}"
    )

    c.drawString(
        100,
        720,
        f"Total Orders: {len(df)}"
    )

    c.save()

    return FileResponse(
        pdf_file,
        media_type="application/pdf",
        filename="sales_report.pdf"
    )
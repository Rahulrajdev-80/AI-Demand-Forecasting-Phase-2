from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session

from app.database.session import SessionLocal

from app.services.upload_service import save_dataset

from app.models.dataset_model import Dataset

from app.utils.jwt_handler import verify_token


router = APIRouter(
    prefix="/api/datasets",
    tags=["Datasets"]
)


# Database Dependency

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# Upload Dataset API

@router.post("/upload")
def upload_dataset(
    file: UploadFile = File(...),
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    dataset = save_dataset(
        db,
        file
    )

    if not dataset:

        raise HTTPException(
            status_code=400,
            detail="Invalid file format"
        )

    return {
        "message": "Dataset uploaded successfully",
        "dataset_id": dataset.id,
        "filename": dataset.filename
    }


# Get All Datasets with Pagination

@router.get("")
def get_datasets(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    skip = (page - 1) * page_size

    datasets = db.query(Dataset)\
        .offset(skip)\
        .limit(page_size)\
        .all()

    total = db.query(Dataset).count()

    return {
        "page": page,
        "page_size": page_size,
        "total_datasets": total,
        "datasets": datasets
    }


# Search Dataset API

@router.get("/search")
def search_datasets(
    search: str,
    email: str = Depends(verify_token),
    db: Session = Depends(get_db)
):

    datasets = db.query(Dataset).filter(
        Dataset.filename.contains(search)
    ).all()

    return {
        "search_keyword": search,
        "results": datasets
    }


# Dataset Filters API

@router.get("/{dataset_id}/filters")
def dataset_filters(
    dataset_id: int,
    email: str = Depends(verify_token)
):

    return {
        "dataset_id": dataset_id,
        "filters": {
            "date_range": True,
            "category": True,
            "region": True,
            "sales_range": True
        }
    }


# Get Single Dataset Details

@router.get("/{dataset_id}")
def get_dataset_by_id(
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

    return dataset


# Delete Dataset API

@router.delete("/{dataset_id}")
def delete_dataset(
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

    db.delete(dataset)

    db.commit()

    return {
        "message": "Dataset deleted successfully"
    }
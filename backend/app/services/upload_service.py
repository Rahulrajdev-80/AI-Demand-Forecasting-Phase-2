import os

import pandas as pd

from fastapi import UploadFile

from sqlalchemy.orm import Session

from app.models.dataset_model import Dataset
from app.models.activity_model import Activity
from app.models.notification_model import Notification


UPLOAD_FOLDER = "app/uploads/datasets"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


def save_dataset(
    db: Session,
    file: UploadFile
):

    file_path = f"{UPLOAD_FOLDER}/{file.filename}"

    # Save uploaded file

    with open(file_path, "wb") as buffer:

        buffer.write(file.file.read())

    # Read CSV or Excel

    if file.filename.endswith(".csv"):

        df = pd.read_csv(
            file_path,
            encoding="latin1"
        )

    elif file.filename.endswith(".xlsx"):

        df = pd.read_excel(file_path)

    else:
        return None

    # Remove duplicates

    df = df.drop_duplicates()

    # Fill missing values

    df = df.fillna(0)

    # Save cleaned dataset

    df.to_csv(
        file_path,
        index=False
    )

    # Store dataset info

    dataset = Dataset(
        filename=file.filename,
        file_path=file_path
        
        )

    db.add(dataset)

    db.commit()

    db.refresh(dataset)

    # Save activity

    activity = Activity(
        action=f"Dataset uploaded: {file.filename}"
    )

    db.add(activity)

    db.commit()

    # Save notification

    notification = Notification(
        message=f"Dataset uploaded: {file.filename}"
    )

    db.add(notification)

    db.commit()

    return dataset
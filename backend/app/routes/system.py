from fastapi import APIRouter

router = APIRouter(
    tags=["System"]
)


@router.get("/api/health")
def health_check():

    return {
        "status": "API Running Successfully"
    }
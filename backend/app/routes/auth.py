from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.database.session import SessionLocal

from app.schemas.user_schema import UserCreate

from app.utils.jwt_handler import (
    verify_token,
    create_access_token
)

from app.services.auth_service import (
    create_user,
    authenticate_user
)

from app.models.user_model import User

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    # Create user

    new_user = create_user(
        db,
        user
    )

    # Set admin role

    new_user.role = "admin"

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "role": new_user.role
        }
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_current_user(
    email: str = Depends(verify_token)
):

    return {
        "message": "Authenticated User",
        "email": email
    }
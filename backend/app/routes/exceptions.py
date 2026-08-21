from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ExceptionRecord
from ..schemas import ExceptionResponse


router = APIRouter(
    prefix="/exceptions",
    tags=["Exceptions"]
)


@router.get(
    "",
    response_model=list[ExceptionResponse]
)
def get_exceptions(
    db: Session = Depends(get_db)
):
    return (
        db.query(ExceptionRecord)
        .order_by(ExceptionRecord.created_at.desc())
        .all()
    )


@router.get(
    "/{exception_id}",
    response_model=ExceptionResponse
)
def get_exception(
    exception_id: str,
    db: Session = Depends(get_db)
):
    return (
        db.query(ExceptionRecord)
        .filter(
            ExceptionRecord.exception_id == exception_id
        )
        .first()
    )

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ExceptionRecord


router = APIRouter(
    prefix="/workflow",
    tags=["Human Review"]
)


@router.post("/{exception_id}/approve")
def approve_exception(
    exception_id: str,
    db: Session = Depends(get_db)
):

    exception = (
        db.query(ExceptionRecord)
        .filter(
            ExceptionRecord.exception_id == exception_id
        )
        .first()
    )

    if exception is None:
        raise HTTPException(
            status_code=404,
            detail="Exception not found"
        )

    exception.status = "APPROVED"
    db.commit()
    db.refresh(exception)

    return {
        "message": "Exception approved by human reviewer",
        "exception_id": exception.exception_id,
        "status": exception.status
    }


@router.post("/{exception_id}/reject")
def reject_exception(
    exception_id: str,
    db: Session = Depends(get_db)
):

    exception = (
        db.query(ExceptionRecord)
        .filter(
            ExceptionRecord.exception_id == exception_id
        )
        .first()
    )

    if exception is None:
        raise HTTPException(
            status_code=404,
            detail="Exception not found"
        )

    exception.status = "REJECTED"
    db.commit()
    db.refresh(exception)

    return {
        "message": "Exception rejected by human reviewer",
        "exception_id": exception.exception_id,
        "status": exception.status
    }

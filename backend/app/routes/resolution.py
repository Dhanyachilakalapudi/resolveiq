from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ExceptionRecord
from ..services.resolution_service import resolve_exception


router = APIRouter(
    prefix="/resolution",
    tags=["Resolution"]
)


@router.post("/{exception_id}")
def analyze_exception(
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

    result = resolve_exception(exception)

    # Backend is the source of truth.
    # Only a successful confidence-gated decision can
    # automatically resolve the exception.
    if result["auto_resolve"]:
        exception.status = "RESOLVED"
        db.commit()
        db.refresh(exception)

    return {
        **result,
        "status": exception.status,
    }

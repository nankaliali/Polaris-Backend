from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from core.database import get_db
from schemas.drive_data_schema import DriveDataRead
from repository.test_data_repository import get_test_data

router = APIRouter()

@router.get("/test-data", response_model=List[DriveDataRead])
def fetch_test_data(
    minLat: Optional[float] = Query(None),
    maxLat: Optional[float] = Query(None),
    minLon: Optional[float] = Query(None),
    maxLon: Optional[float] = Query(None),
    skip: int = Query(0, ge=0),
    limit: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    return get_test_data(db, minLat, maxLat, minLon, maxLon, skip, limit)

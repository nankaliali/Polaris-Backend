from typing import Optional
from sqlalchemy.orm import Session
from models.drive_data_model import DriveData

def get_test_data(
    db: Session,
    minLat: float = None,
    maxLat: float = None,
    minLon: float = None,
    maxLon: float = None,
    skip: int = 0,
    limit: int = None 
):
    query = db.query(DriveData)

    if minLat is not None and maxLat is not None:
        query = query.filter(DriveData.latitude >= minLat, DriveData.latitude <= maxLat)
    if minLon is not None and maxLon is not None:
        query = query.filter(DriveData.longitude >= minLon, DriveData.longitude <= maxLon)

    query = query.order_by(DriveData.timestamp).offset(skip)

    if limit is not None:
        query = query.limit(limit)  
    print(">> get_test_data: limit:", limit)


    return query.all()

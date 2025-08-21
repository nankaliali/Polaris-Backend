from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from core.database import get_db
from core.dependencies import get_current_user
from models.drive_data_model import User
from repository.user_repository import get_user_by_device_id
from schemas.drive_data_schema import CellularData, DriveDataRead, DriveDataResponse
from repository.drive_data_repository import create_drive_data, get_all_drive_data_repo, get_data_in_bbox, get_drive_data_by_id, get_drive_data_for_admin, get_drive_data_for_device
from typing import List, Optional
from fastapi import Query
from fastapi import APIRouter
router = APIRouter()

@router.get("/drive-data", response_model=List[DriveDataRead])
def fetch_drive_data_by_bbox(
    minLat: float = Query(...),
    maxLat: float = Query(...),
    minLon: float = Query(...),
    maxLon: float = Query(...),
    db: Session = Depends(get_db),
):
    data = get_data_in_bbox(db, minLat, maxLat, minLon, maxLon)
    return data


@router.post(
    "/drive-data/app",
    response_model=DriveDataRead,
    status_code=status.HTTP_201_CREATED,
)
async def insert_drive_data(
    data: list[CellularData],
    db: Session = Depends(get_db),
):
    
    for d in data:
        d = DriveDataRead(
            id=d.id,
            latitude=d.latitude,
            longitude=d.longitude,
            timestamp=d.timestamp,
            technology=d.technology,
            plmnId=d.plmnId,
            lac=d.lac,
            rac=d.rac,
            tac=d.tac,
            cellId=d.cellId,
            frequencyBand=d.frequencyBand,
            arfcn=d.arfcn,
            actualFrequency=d.actualFrequency,
            rsrp=d.rsrp,
            rsrq=d.rsrq,
            rscp=d.rscp,
            ecNo=d.ecNo,
            rxLev=d.rxLev,
            sinr=d.sinr,
            operatorName=d.operatorName,
            notes=d.notes,
            httpUploadRate=float(d.httpUploadRate),
            pingResponseTime=str(d.pingResponseTime),
            dnsResponseTime=str(d.dnsResponseTime),
            webResponseTime=str(d.webResponseTime),
            smsDeliveryTime=str(d.smsDeliveryTime),
            testNotes=d.testNotes,
            device_id=d.deviceId,  
        )

        d = create_drive_data(db, d)

    return d




@router.get("/drive-data/", response_model=list[DriveDataResponse])
async def get_all_drive_data(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Get all drive data"""
    
    return get_all_drive_data_repo(db=db, skip=skip, limit=limit)




@router.get(
    "/user-drive-test-data/",
    response_model=List[DriveDataResponse],
    summary="List all drive-test data for the current user",
    tags=["drive-test-data"],
)
async def list_user_drive_test_data(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max number of records to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve a paginated list of all drive-test data records belonging to the authenticated user.
    """

    return get_drive_data_for_device(
        db=db,
        device_id=current_user.device_id,
        skip=skip,
        limit=limit,
    )



@router.get(
    "/drive-data/admin",
    response_model=List[DriveDataResponse],
    summary="Admin: list all drive-data",
    tags=["drive-data", "admin"],
)
async def list_all_drive_data_admin(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: Optional[int] = Query(None, ge=1, description="Max records to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve **all** drive-data records (optionally paginated).
    Only users with username 'admin@polaris' are allowed.
    """
    if current_user.username != "admin@polaris":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access all drive data"
        )

    return get_drive_data_for_admin(db=db, skip=skip, limit=limit)

@router.post(
    "/drive-data/upload-test",
    summary="Test file upload endpoint",
    tags=["testing"],
    status_code=status.HTTP_200_OK,
)
async def upload_test_file(
    file: UploadFile = File(...),
):
    """
    Test endpoint for uploading a file.
    Reads the entire file into memory (for testing) and returns filename, content type, and size.
    """
    try:
        contents = await file.read()
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": len(contents),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read uploaded file: {e}"
        )
    finally:
        await file.close()
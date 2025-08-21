from sqlalchemy.orm import Session
from models.drive_data_model import DriveData
from schemas.drive_data_schema import DriveDataRead



def get_data_in_bbox(db: Session, minLat: float, maxLat: float, minLon: float, maxLon: float):
    return db.query(DriveData).filter(
        DriveData.latitude >= minLat,
        DriveData.latitude <= maxLat,
        DriveData.longitude >= minLon,
        DriveData.longitude <= maxLon
    ).all()


def create_drive_data(db: Session, drive_data: DriveDataRead) -> DriveData:
    """
    Create and persist a new DriveData row,
    linking it by device_id (which is a FK to users.device_id).
    """
    db_drive = DriveData(
        device_id        = drive_data.device_id,
        latitude         = drive_data.latitude,
        longitude        = drive_data.longitude,
        timestamp        = drive_data.timestamp,
        technology       = drive_data.technology,
        plmnId           = drive_data.plmnId,
        lac              = drive_data.lac,
        rac              = drive_data.rac,
        tac              = drive_data.tac,
        cellId           = drive_data.cellId,
        frequencyBand    = drive_data.frequencyBand,
        arfcn            = drive_data.arfcn,
        actualFrequency  = drive_data.actualFrequency,
        rsrp             = drive_data.rsrp,
        rsrq             = drive_data.rsrq,
        rscp             = drive_data.rscp,
        ecNo             = drive_data.ecNo,
        rxLev            = drive_data.rxLev,
        sinr             = drive_data.sinr,
        operatorName     = drive_data.operatorName,
        notes            = drive_data.notes,
        httpUploadRate   = drive_data.httpUploadRate,
        pingResponseTime = drive_data.pingResponseTime,
        dnsResponseTime  = drive_data.dnsResponseTime,
        webResponseTime  = drive_data.webResponseTime,
        smsDeliveryTime  = drive_data.smsDeliveryTime,
        testNotes        = drive_data.testNotes,
    )
    db.add(db_drive)
    db.commit()
    db.refresh(db_drive)
    return db_drive

def get_drive_data_by_id(db: Session, drive_data_id: int):
    """Get drive data by ID"""
    return db.query(DriveData).filter(DriveData.id == drive_data_id).first()

def get_drive_data_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get drive data for a specific user"""
    return db.query(DriveData).filter(DriveData.user_id == user_id).offset(skip).limit(limit).all()

def get_all_drive_data_repo(db: Session, skip: int = 0, limit: int = 100):
    """Get all drive data"""
    return db.query(DriveData).offset(skip).limit(limit).all()



def get_drive_data_for_device(
    db: Session,
    device_id: str,
    skip: int = 0,
    limit: int = 100
):
    return (
        db.query(DriveData)
          .filter(DriveData.device_id == device_id)
          .order_by(DriveData.timestamp)
          .offset(skip)
          .limit(limit)
          .all()
    )

def get_drive_data_for_admin(
    db: Session,
    skip: int = 0,
    limit: int = 100
):
    return (
        db.query(DriveData)
          .order_by(DriveData.timestamp)
          .offset(skip)
          .limit(limit)
          .all()
    )

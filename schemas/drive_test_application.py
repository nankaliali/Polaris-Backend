from typing import Optional
from pydantic import BaseModel

class DriveDataRead(BaseModel):
    id: int
    latitude: float
    longitude: float
    timestamp: int
    technology: str
    plmnId: int
    lac: int
    rac: int
    tac: int
    cellId: int
    frequencyBand: str
    arfcn: int
    actualFrequency: str
    rsrp: int
    rsrq: int
    rscp: int
    ecNo: float
    rxLev: float
    sinr: float
    operatorName: str
    notes: Optional[str] = None
    httpUploadRate: Optional[float] = None
    pingResponseTime: Optional[str] = None
    dnsResponseTime: Optional[str] = None
    webResponseTime: Optional[str] = None
    smsDeliveryTime: Optional[str] = None
    testNotes: Optional[str] = None
    device_id: Optional[str] = None    

    class Config:
        from_attributes = True  # Pydantic v2; if error, use orm_mode = True

from typing import Optional

from pydantic import BaseModel

class CellularData(BaseModel):
    id: int
    deviceId: str
    timestamp: int
    timestampFormatted: str
    latitude: float
    longitude: float
    technology: str
    plmnId: str
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
    ecNo: int
    rxLev: int
    sinr: int
    operatorName: str
    notes: str
    httpUploadRate: float
    pingResponseTime: float
    dnsResponseTime: float
    webResponseTime: float
    smsDeliveryTime: float
    testNotes: str

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
    device_id: str 


    class Config:
        from_attributes = True  # برای پایدانتیک v2؛ اگه ارور داد بذار orm_mode = True



class DriveDataResponse(BaseModel):
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
        from_attributes = True

from sqlalchemy.orm import relationship
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DriveData(Base):
    __tablename__ = "drive_data"
    __allow_unmapped__ = True  
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(BigInteger)
    technology = Column(String)
    plmnId = Column(Integer)
    lac = Column(Integer)
    rac = Column(Integer)
    tac = Column(Integer)
    cellId = Column(Integer)
    frequencyBand = Column(String)
    arfcn = Column(Integer)
    actualFrequency = Column(String)
    rsrp = Column(Integer)
    rsrq = Column(Integer)
    rscp = Column(Integer)
    ecNo = Column(Float)
    rxLev = Column(Float)
    sinr = Column(Float)
    operatorName = Column(String)
    notes = Column(String, nullable=True)
    httpUploadRate = Column(Float, nullable=True)
    pingResponseTime = Column(String, nullable=True)
    dnsResponseTime = Column(String, nullable=True)
    webResponseTime = Column(String, nullable=True)
    smsDeliveryTime = Column(String, nullable=True)
    testNotes = Column(String, nullable=True)
    device_id  = Column(String(256), ForeignKey("users.device_id"), nullable=False, index=True)


    user = relationship("User", back_populates="drive_data")



class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)  

    # a unique-per-user string identifier for their device
    device_id = Column(String(256), unique=True, nullable=False, index=True)

    # collection of all DriveData rows for this device/user
    drive_data = relationship("DriveData", back_populates="user")

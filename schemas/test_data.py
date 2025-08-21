from pydantic import BaseModel

class TestDataSchema(BaseModel):
    id: int
    timestamp: int
    latitude: float
    longitude: float
    operator_name: str | None = None
    http_upload_rate: float | None = None
    ping_response_time: str | None = None
    dns_response_time: str | None = None
    web_response_time: str | None = None
    sms_delivery_time: str | None = None
    notes: str | None = None
    test_notes: str | None = None

    class Config:
        orm_mode = True

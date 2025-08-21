import csv
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.drive_data_model import DriveData

CSV_FILE = "cellular_data.csv"
db: Session = SessionLocal()

with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')

    for row in reader:
        try:
            drive_data = DriveData(
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
                timestamp=int(row["timestamp"]),
                technology=row["technology"],
                plmnId=int(row["plmn_id"]),
                lac=int(row["lac"]),
                rac=int(row["rac"]),
                tac=int(row["tac"]),
                cellId=int(row["cell_id"]),
                frequencyBand=row["frequency_band"],
                arfcn=int(row["arfcn"]),
                actualFrequency=row["actual_frequency"],
                rsrp=int(row["rsrp"]),
                rsrq=int(row["rsrq"]),
                rscp=int(row["rscp"]),
                ecNo=float(row["ec_no"]),
                rxLev=float(row["rx_lev"]),
                sinr=float(row["sinr"]),
                operatorName=row.get("operator_name"),
                notes=row.get("notes"),
                httpUploadRate=float(row["http_upload_rate"]) if row["http_upload_rate"] else None,
                pingResponseTime=row.get("ping_response_time"),
                dnsResponseTime=row.get("dns_response_time"),
                webResponseTime=row.get("web_response_time"),
                smsDeliveryTime=row.get("sms_delivery_time"),
                testNotes=row.get("test_notes"),
                device_id=row.get("deviceId")
            )
            db.add(drive_data)
        except Exception as e:
            print(f" Error in row: {row}")
            print(f"Reason: {e}")

db.commit()
db.close()
print(" CSV data imported successfully!")

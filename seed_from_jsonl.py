import json
from sqlalchemy.orm import Session
from core.database import SessionLocal
from core.security import hash_password
from models.drive_data_model import DriveData
from repository.user_repository import create_user, get_user_by_device_id

JSON_FILE = "polaris_cellular_data_20250608_100027.jsonl"
db: Session = SessionLocal()

with open(JSON_FILE, 'r', encoding='utf-8') as f:
    raw = f.read()

# جدا کردن هر شیء JSON
json_objects = raw.strip().split('\n}\n')
json_objects = [obj + '}' if not obj.endswith('}') else obj for obj in json_objects]

for obj_str in json_objects:
    try:
        row = json.loads(obj_str)

        user = get_user_by_device_id(db, row.get("deviceId"))
        if user is None:
            pw_hash = hash_password("123123123")

            user = create_user(
                db,
                username="username_jsonl",
                hashed_password=pw_hash,
                device_id=row.get("deviceId"),
            )
        





        drive_data = DriveData(
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            timestamp=int(row["timestamp"]),
            technology=row["technology"],
            plmnId = int(row["plmnId"]) if row["plmnId"] != "" else -1,
            lac=int(row["lac"]),
            rac=int(row["rac"]),
            tac=int(row["tac"]),
            cellId=int(row["cellId"]),
            frequencyBand=row["frequencyBand"],
            arfcn=int(row["arfcn"]),
            actualFrequency=row["actualFrequency"],
            rsrp=int(row["rsrp"]),
            rsrq=int(row["rsrq"]),
            rscp=int(row["rscp"]),
            ecNo=float(row["ecNo"]),
            rxLev=float(row["rxLev"]),
            sinr=float(row["sinr"]),
            operatorName=row.get("operatorName"),
            notes=row.get("notes"),
            httpUploadRate=float(row["httpUploadRate"]) if row.get("httpUploadRate") is not None else None,
            pingResponseTime=float(row["pingResponseTime"]) if row.get("pingResponseTime") is not None else None,
            dnsResponseTime=float(row["dnsResponseTime"]) if row.get("dnsResponseTime") is not None else None,
            webResponseTime=float(row["webResponseTime"]) if row.get("webResponseTime") is not None else None,
            smsDeliveryTime=float(row["smsDeliveryTime"]) if row.get("smsDeliveryTime") is not None else None,
            testNotes=row.get("testNotes"),
            device_id=row.get("deviceId")
        )

        db.add(drive_data)
    except Exception as e:
        print(f"❌ Error in row:\n{obj_str}")
        print(f"Reason: {e}")

db.commit()
db.close()
print("✅ JSON data imported successfully!")

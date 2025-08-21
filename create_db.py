from sqlalchemy import create_engine
from models.drive_data_model import Base

DATABASE_URL = "sqlite:///./test.db" 
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)
print("Tables created.")

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import DeviceData, DeviceDataCalculatedDim
from mqtt.client import mqtt_client
from sqlalchemy.future import select

app = FastAPI()

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup():
    create_tables()
    await mqtt_client.start()

@app.get("/api/device_data/")
def get_device_data(db: Session = Depends(get_db)):
    result = db.execute(select(DeviceData))
    return result.scalars().all()

@app.get("/api/device_data_calculated_dim/")
def get_device_data(db: Session = Depends(get_db)):
    result = db.execute(select(DeviceDataCalculatedDim))
    return result.scalars().all()
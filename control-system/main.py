from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal, engine, Base
from models import DeviceData
from mqtt.client import mqtt_client
from sqlalchemy.future import select

app = FastAPI()

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup():
    await create_tables()
    await mqtt_client.start()

@app.get("/api/devices/")
async def get_device_data(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DeviceData))
    return result.scalars().all()
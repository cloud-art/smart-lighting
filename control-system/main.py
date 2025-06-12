from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import api
from core.db import Base, engine
from core.dependencies.mqtt import get_mqtt_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()    
    mqtt_client = get_mqtt_client()
    try:
        await mqtt_client.start()
        yield
    finally:
        pass

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://0.0.0.0",
    "http://0.0.0.0:8080",
    "http://213.108.20.168",
    "http://213.108.20.168:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_tables():
    Base.metadata.create_all(bind=engine)

app.include_router(api.router, prefix="/api")
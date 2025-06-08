from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import api
from core.db import Base, engine
from core.dependencies import get_mqtt_client
from services.mqtt.client import MQTTClient

app = FastAPI()

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
    from core.initial_data import init_devices

    Base.metadata.create_all(bind=engine)
    init_devices()


@app.on_event("startup")
async def startup(mqtt_client: MQTTClient = Depends(get_mqtt_client())):
    create_tables()
    await mqtt_client.start()


app.include_router(api.router, prefix="/api")

from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.orm import Session

from core.config import settings
from core.db import SessionLocal
from repositories.device import DeviceRepository
from repositories.device_data import DeviceDataRepository
from repositories.device_data_calculated_dim import DeviceDataCalculatedDimRepository
from repositories.device_data_corrected_dim import DeviceDataCorrectedDimRepository
from repositories.device_data_summary import DeviceDataSummaryRepository
from repositories.device_stats import DeviceStatsRepository
from services.ai_model import AiModel
from services.mqtt.client import MQTTClient
from services.mqtt.handlers import MessageHandler


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_mqtt_handler() -> MessageHandler:
    return MessageHandler()


def get_mqtt_client(handler: MessageHandler = Depends(get_mqtt_handler)) -> MQTTClient:
    return MQTTClient(handler)


async def get_async_mqtt_client(
    client: MQTTClient = Depends(get_mqtt_client),
) -> AsyncGenerator[MQTTClient, None]:
    try:
        await client.start()
        yield client
    finally:
        await client.disconnect()


def get_ai_model() -> AiModel:
    return AiModel(settings.MODEL_PATH)


def get_device_data_repository(db: Session = Depends(get_db)) -> DeviceDataRepository:
    return DeviceDataRepository(db)


def get_device_data_calculated_dim_repository(
    db: Session = Depends(get_db),
) -> DeviceDataCalculatedDimRepository:
    return DeviceDataCalculatedDimRepository(db)


def get_device_data_corrected_dim_repository(
    db: Session = Depends(get_db),
) -> DeviceDataCorrectedDimRepository:
    return DeviceDataCorrectedDimRepository(db)


def get_device_data_summary_repository(
    db: Session = Depends(get_db),
) -> DeviceDataSummaryRepository:
    return DeviceDataRepository(db)


def get_device_stats_repository(db: Session = Depends(get_db)) -> DeviceStatsRepository:
    return DeviceDataRepository(db)


def get_device_repository(db: Session = Depends(get_db)) -> DeviceRepository:
    return DeviceRepository(db)


DeviceDataRepoDep = Annotated[DeviceDataRepository, Depends(get_device_data_repository)]
DeviceDataRepoDep = Annotated[
    DeviceDataCalculatedDimRepository,
    Depends(get_device_data_calculated_dim_repository),
]
DeviceDataRepoDep = Annotated[
    DeviceDataCorrectedDimRepository, Depends(get_device_data_corrected_dim_repository)
]
DeviceDataRepoDep = Annotated[
    DeviceDataSummaryRepository, Depends(get_device_data_summary_repository)
]
DeviceDataRepoDep = Annotated[
    DeviceStatsRepository, Depends(get_device_stats_repository)
]
DeviceDataRepoDep = Annotated[DeviceRepository, Depends(get_device_repository)]

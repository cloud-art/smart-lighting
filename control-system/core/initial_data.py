from fastapi import Depends
from sqlalchemy.orm import Session

from core.dependencies.db import get_db
from models.device import DeviceModel


def init_devices(db: Session = Depends(get_db)):
    first_device = db.query(DeviceModel).filter(DeviceModel.serial_number == "1")
    seconds_device = db.query(DeviceModel).filter(DeviceModel.serial_number == "2")

    if first_device.count == 0:
        db.add(
            DeviceModel(
                mqtt_topic="devices/1",
                control_type="simple_rules",
                serial_number="1",
                lighting_class="B1",
                latitude=47.22486,
                longitude=39.702285,
            )
        )
        db.commit()

    if seconds_device.count == 0:
        db.add(
            DeviceModel(
                mqtt_topic="devices/2",
                control_type="ai_model",
                serial_number="2",
                lighting_class="B1",
                latitude=47.22486,
                longitude=39.702285,
            )
        )
        db.commit()

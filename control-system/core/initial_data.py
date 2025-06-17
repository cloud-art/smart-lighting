from sqlalchemy.orm import Session

from models.device import DeviceModel


def init_devices(db: Session):
    first_device = db.query(DeviceModel).filter(
        DeviceModel.serial_number == "test_device_1"
    )
    seconds_device = db.query(DeviceModel).filter(
        DeviceModel.serial_number == "test_device_2"
    )

    if first_device.count == 0:
        db.add(
            DeviceModel(
                control_type="simple_rules",
                serial_number="test_device_1",
                lighting_class="B1",
                latitude=47.22486,
                longitude=39.702285,
            )
        )
        db.commit()

    if seconds_device.count == 0:
        db.add(
            DeviceModel(
                control_type="ai_model",
                serial_number="test_device_2",
                lighting_class="B1",
                latitude=47.22486,
                longitude=39.702285,
            )
        )
        db.commit()

import csv
import io
from datetime import datetime, timedelta

from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.device_data import DeviceData, DeviceDataCorrectedDim


class ExportsService:
    @staticmethod
    def _execute_stats_query(db: Session, days: int, serial_number: int):
        query = select(
            DeviceData,
            DeviceDataCorrectedDim.dimming_level.label("corrected_dimming_level"),
        ).join(
            DeviceDataCorrectedDim,
            DeviceData.id == DeviceDataCorrectedDim.device_data_id,
        )

        if days is not None:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            query = query.where(DeviceData.timestamp.between(start_date, end_date))

        if serial_number is not None:
            query = query.where(DeviceData.serial_number == serial_number)

        result = db.execute(query)
        data = result.all()

        output = io.StringIO()
        writer = csv.writer(output)

        headers = [
            "id",
            "timestamp",
            "serial_number",
            "latitude",
            "longitude",
            "car_count",
            "traffic_speed",
            "traffic_density",
            "pedestrian_count",
            "pedestrian_density",
            "ambient_light",
            "lighting_class",
            "lamp_power",
            "weather",
            "dimming_level",
        ]
        writer.writerow(headers)

        for row in data:
            device_data = row.DeviceData
            writer.writerow(
                [
                    device_data.id,
                    device_data.timestamp.isoformat(),
                    device_data.serial_number,
                    device_data.latitude,
                    device_data.longitude,
                    device_data.car_count,
                    device_data.traffic_speed,
                    device_data.traffic_density,
                    device_data.pedestrian_count,
                    device_data.pedestrian_density,
                    device_data.ambient_light,
                    device_data.lighting_class,
                    device_data.lamp_power,
                    device_data.weather,
                    row.corrected_dimming_level,
                ]
            )

        output.seek(0)

        filename = (
            f"device_data_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

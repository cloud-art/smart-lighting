import csv
import io
from datetime import datetime, timezone
from typing import Optional

from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from repositories.device_data_summary import DeviceDataSummaryRepository
from schemas.device_data import DeviceDataSummarySchema


class DeviceDataExportsService:
    CSV_HEADERS = [
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

    def __init__(self, db: Session):
        self.summary_repository = DeviceDataSummaryRepository(db)

    def export_to_csv(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = datetime.now(tz=timezone.utc),
        device: Optional[int] = None,
    ) -> StreamingResponse:
        data = self.summary_repository.get_all(
            start_date=start_date, end_date=end_date, device_id=device
        )

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(self.CSV_HEADERS)

        validated_data = [DeviceDataSummarySchema.model_validate(row) for row in data]

        for device_data in validated_data:
            writer.writerow(self.summary_to_csv_row(device_data))

        output.seek(0)
        return self._create_streaming_response(output)

    def _create_streaming_response(self, output: io.StringIO) -> StreamingResponse:
        filename = f"device_data_export_{datetime.now(tz=timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv"
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    def summary_to_csv_row(self, data: DeviceDataSummarySchema):
        corrected_dimming_level = data.corrected_dimming_level

        return [
            data.id,
            data.timestamp.isoformat(),
            data.device.serial_number,
            data.device.latitude,
            data.device.longitude,
            data.car_count,
            data.traffic_speed,
            data.traffic_density,
            data.pedestrian_count,
            data.pedestrian_density,
            data.ambient_light,
            data.device.lighting_class,
            data.lamp_power,
            data.weather,
            corrected_dimming_level.dimming_level
            if corrected_dimming_level is not None
            else None,
        ]

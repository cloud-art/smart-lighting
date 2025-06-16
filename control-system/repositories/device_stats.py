from datetime import datetime
from typing import Optional, Sequence

from sqlalchemy import Row, extract, func, select
from sqlalchemy.orm import Session

from core.types import SQLExtractFields
from models.device_data import DeviceDataModel
from models.device_data_calculated_dim import DeviceDataCalculatedDimModel
from models.device_data_corrected_dim import DeviceDataCorrectedDimModel


class DeviceStatsRepository:
    def __init__(self, db: Session):
        self.db = db

    def _query(
        self,
        time_unit: SQLExtractFields,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        device: Optional[int] = None,
    ):
        time_extract = extract(time_unit.value, DeviceDataModel.timestamp).label(
            time_unit.value
        )

        query = (
            select(
                time_extract,
                func.avg(DeviceDataModel.car_count).label("avg_car_count"),
                func.avg(DeviceDataModel.traffic_speed).label("avg_traffic_speed"),
                func.avg(DeviceDataModel.pedestrian_count).label(
                    "avg_pedestrian_count"
                ),
                func.avg(DeviceDataModel.dimming_level).label("avg_dimming_level"),
                func.avg(DeviceDataCalculatedDimModel.dimming_level).label(
                    "avg_calculated_dim"
                ),
                func.avg(DeviceDataCorrectedDimModel.dimming_level).label(
                    "avg_corrected_dim"
                ),
            )
            .outerjoin(
                DeviceDataCalculatedDimModel,
                DeviceDataModel.id == DeviceDataCalculatedDimModel.device_data_id,
            )
            .outerjoin(
                DeviceDataCorrectedDimModel,
                DeviceDataModel.id == DeviceDataCorrectedDimModel.device_data_id,
            )
        )

        conditions = []
        if start_date is not None:
            conditions.append(DeviceDataModel.timestamp >= start_date)
        if end_date is not None:
            conditions.append(DeviceDataModel.timestamp <= end_date)
        if device is not None:
            conditions.append(DeviceDataModel.device_id == device)

        if conditions:
            query = query.where(*conditions)

        query = query.group_by(time_extract).order_by(time_extract)

        return query

    def get_hourly_stats(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        device: Optional[int] = None,
    ) -> Sequence[Row]:
        return self.db.execute(
            self._query(SQLExtractFields.Hour, start_date, end_date, device)
        ).all()

    def get_weekday_stats(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        device: Optional[int] = None,
    ) -> Sequence[Row]:
        return self.db.execute(
            self._query(SQLExtractFields.Weekday, start_date, end_date, device)
        ).all()

    def get_daily_stats(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        device: Optional[int] = None,
    ) -> Sequence[Row]:
        return self.db.execute(
            self._query(SQLExtractFields.Day, start_date, end_date, device)
        ).all()

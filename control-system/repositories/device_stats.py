from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from models.device_data import DeviceDataModel
from models.device_data_calculated_dim import DeviceDataCalculatedDimModel
from models.device_data_corrected_dim import DeviceDataCorrectedDimModel
from schemas.device_stats import DailyStats, HourlyStats, WeekdayStats


class DeviceStatsRepository:
    def __init__(self, db: Session):
        self.db = db

    def _execute_stats_query(
        self, time_unit: str, start_date: datetime, end_date: datetime
    ) -> List[Any]:
        time_extract = extract(time_unit, DeviceDataModel.timestamp).label(time_unit)

        return self.db.execute(
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
            .where(DeviceDataModel.timestamp.between(start_date, end_date))
            .group_by(time_unit)
            .order_by(time_unit)
        ).all()

    def get_hourly_stats(
        self, start_date: datetime, end_date: datetime
    ) -> List[HourlyStats]:
        data = self._execute_stats_query("hour", start_date, end_date)
        return HourlyStats.model_validate(data)

    def get_weekday_stats(
        self, start_date: datetime, end_date: datetime
    ) -> List[WeekdayStats]:
        data = self._execute_stats_query("dow", start_date, end_date)
        return WeekdayStats.model_validate(data)

    def get_daily_stats(
        self, start_date: datetime, end_date: datetime
    ) -> List[DailyStats]:
        data = self._execute_stats_query("day", start_date, end_date)
        return DailyStats.model_validate(data)

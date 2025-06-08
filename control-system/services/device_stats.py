from datetime import datetime, timedelta
from typing import List

from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from models.device_data import (
    DeviceData,
    DeviceDataCalculatedDim,
    DeviceDataCorrectedDim,
)


class DeviceStatsService:
    @staticmethod
    def _execute_stats_query(
        db: Session, time_unit: str, start_date: datetime, end_date: datetime
    ):
        time_extract = extract(time_unit, DeviceData.timestamp).label(time_unit)

        return db.execute(
            select(
                time_extract,
                func.avg(DeviceData.car_count).label("avg_car_count"),
                func.avg(DeviceData.traffic_speed).label("avg_traffic_speed"),
                func.avg(DeviceData.pedestrian_count).label("avg_pedestrian_count"),
                func.avg(DeviceData.dimming_level).label("avg_dimming_level"),
                func.avg(DeviceDataCalculatedDim.dimming_level).label(
                    "avg_calculated_dim"
                ),
                func.avg(DeviceDataCorrectedDim.dimming_level).label(
                    "avg_corrected_dim"
                ),
            )
            .outerjoin(
                DeviceDataCalculatedDim,
                DeviceData.id == DeviceDataCalculatedDim.device_data_id,
            )
            .outerjoin(
                DeviceDataCorrectedDim,
                DeviceData.id == DeviceDataCorrectedDim.device_data_id,
            )
            .where(DeviceData.timestamp.between(start_date, end_date))
            .group_by(time_unit)
            .order_by(time_unit)
        )

    @staticmethod
    def get_hourly_averages(db: Session, days: int = 30) -> List[dict]:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        result = DeviceStatsService._execute_stats_query(
            db, "hour", start_date, end_date
        )

        return [
            {"hour": row.hour, **DeviceStatsService._process_stats_row(row)}
            for row in result
        ]

    @staticmethod
    def get_weekday_averages(db: Session, weeks: int = 12) -> List[dict]:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(weeks=weeks)

        result = DeviceStatsService._execute_stats_query(
            db, "dow", start_date, end_date
        )

        weekday_names = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        return [
            {
                "day": int(row.dow),
                "day_name": weekday_names[int(row.dow)],
                **DeviceStatsService._process_stats_row(row),
            }
            for row in result
        ]

    @staticmethod
    def get_daily_averages(db: Session, months: int = 6) -> List[dict]:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30 * months)

        result = DeviceStatsService._execute_stats_query(
            db, "day", start_date, end_date
        )

        return [
            {"day_of_month": int(row.day), **DeviceStatsService._process_stats_row(row)}
            for row in result
        ]

    @staticmethod
    def _process_stats_row(row):
        return {
            "avg_car_count": (
                float(row.avg_car_count) if row.avg_car_count is not None else None
            ),
            "avg_traffic_speed": (
                float(row.avg_traffic_speed)
                if row.avg_traffic_speed is not None
                else None
            ),
            "avg_pedestrian_count": (
                float(row.avg_pedestrian_count)
                if row.avg_pedestrian_count is not None
                else None
            ),
            "avg_dimming_level": (
                float(row.avg_dimming_level)
                if row.avg_dimming_level is not None
                else None
            ),
            "avg_calculated_dim": (
                float(row.avg_calculated_dim)
                if row.avg_calculated_dim is not None
                else None
            ),
            "avg_corrected_dim": (
                float(row.avg_corrected_dim)
                if row.avg_corrected_dim is not None
                else None
            ),
        }

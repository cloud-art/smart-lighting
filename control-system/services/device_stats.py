from datetime import datetime, timedelta, timezone
from typing import Sequence

from sqlalchemy.orm import Session

from core.types import SQLExtractFields
from repositories.device_stats import DeviceStatsRepository
from schemas.device_stats import (
    DeviceDailyAverageStats,
    DeviceHourlyAveragesStats,
    DeviceStatsRowSchema,
    DeviceWeekdayAverageStats,
)
from utils.time import format_dow_number


class DeviceStatsService:
    def __init__(self, db: Session):
        self.repository = DeviceStatsRepository(db)

    def get_hourly_averages(
        self, days: int = 30
    ) -> Sequence[DeviceHourlyAveragesStats]:
        end_date = datetime.now(tz=timezone.utc)
        start_date = end_date - timedelta(days=days)

        result = self.repository.get_hourly_stats(
            start_date=start_date, end_date=end_date
        )

        return [
            DeviceHourlyAveragesStats.model_validate(
                {
                    "hour": row.hour,
                    **DeviceStatsRowSchema.model_validate(row),
                }
            )
            for row in result
        ]

    def get_weekday_averages(
        self, weeks: int = 12
    ) -> Sequence[DeviceWeekdayAverageStats]:
        end_date = datetime.now(tz=timezone.utc)
        start_date = end_date - timedelta(weeks=weeks)

        result = self.repository.get_weekday_stats(
            start_date=start_date, end_date=end_date
        )

        return [
            DeviceWeekdayAverageStats.model_validate(
                {
                    "day": int(row[SQLExtractFields.Weekday.value]),
                    "day_name": format_dow_number(row[SQLExtractFields.Weekday.value]),
                    **DeviceStatsRowSchema.model_validate(row),
                }
            )
            for row in result
        ]

    def get_daily_averages(self, months: int = 6) -> Sequence[DeviceDailyAverageStats]:
        end_date = datetime.now(tz=timezone.utc)
        start_date = end_date - timedelta(days=30 * months)

        result = self.repository.get_daily_stats(
            start_date=start_date, end_date=end_date
        )

        return [
            DeviceDailyAverageStats.model_validate(
                {
                    "day_of_month": row[SQLExtractFields.Day],
                    **DeviceStatsRowSchema.model_validate(row),
                }
            )
            for row in result
        ]

from datetime import datetime, timezone
from typing import Optional, Sequence

from sqlalchemy.orm import Session

from core.types import SQLExtractFields
from repositories.device_stats import DeviceStatsRepository
from schemas.device_stats import (
    DeviceDailyAverageStats,
    DeviceHourlyAveragesStats,
    DeviceWeekdayAverageStats,
)
from utils.time import format_dow_number


class DeviceStatsService:
    def __init__(self, db: Session):
        self.repository = DeviceStatsRepository(db)

    def get_hourly_averages(
        self,
        device: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: datetime = datetime.now(tz=timezone.utc),
    ) -> Sequence[DeviceHourlyAveragesStats]:
        result = self.repository.get_hourly_stats(
            start_date=start_date, end_date=end_date, device=device
        )

        return [
            DeviceHourlyAveragesStats.model_validate(
                {
                    "hour": row._asdict()[SQLExtractFields.Hour.value],
                    **row._asdict(),
                }
            )
            for row in result
        ]

    def get_weekday_averages(
        self,
        device: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: datetime = datetime.now(tz=timezone.utc),
    ) -> Sequence[DeviceWeekdayAverageStats]:
        result = self.repository.get_weekday_stats(
            start_date=start_date, end_date=end_date, device=device
        )

        return [
            DeviceWeekdayAverageStats.model_validate(
                {
                    "day": int(row._asdict()[SQLExtractFields.Weekday.value]),
                    "day_name": format_dow_number(
                        row._asdict()[SQLExtractFields.Weekday.value]
                    ),
                    **row._asdict(),
                }
            )
            for row in result
        ]

    def get_daily_averages(
        self,
        device: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: datetime = datetime.now(tz=timezone.utc),
    ) -> Sequence[DeviceDailyAverageStats]:
        result = self.repository.get_daily_stats(
            start_date=start_date, end_date=end_date, device=device
        )

        return [
            DeviceDailyAverageStats.model_validate(
                {
                    "day_of_month": row._asdict()[SQLExtractFields.Day.value],
                    **row._asdict(),
                }
            )
            for row in result
        ]

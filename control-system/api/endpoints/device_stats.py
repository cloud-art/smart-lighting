from datetime import datetime
from typing import List, Optional, Sequence

from fastapi import APIRouter, Depends

from core.dependencies.service import get_device_stats_service
from schemas.device_stats import (
    DeviceDailyAverageStats,
    DeviceHourlyAveragesStats,
    DeviceWeekdayAverageStats,
)
from services.device_stats import DeviceStatsService

router = APIRouter(prefix="/device-stats", tags=["Device Statistics"])


@router.get("/hourly-averages/", response_model=List[DeviceHourlyAveragesStats])
def get_hourly_averages(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    device: Optional[int] = None,
    service: DeviceStatsService = Depends(get_device_stats_service),
):
    return service.get_hourly_averages(
        start_date=start_date, end_date=end_date, device=device
    )


@router.get("/weekday-averages/", response_model=List[DeviceWeekdayAverageStats])
def get_weekday_averages(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    device: Optional[int] = None,
    service: DeviceStatsService = Depends(get_device_stats_service),
):
    return service.get_weekday_averages(
        start_date=start_date, end_date=end_date, device=device
    )


@router.get("/daily-averages/", response_model=Sequence[DeviceDailyAverageStats])
def get_daily_averages(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    device: Optional[int] = None,
    service: DeviceStatsService = Depends(get_device_stats_service),
):
    return service.get_daily_averages(
        start_date=start_date, end_date=end_date, device=device
    )

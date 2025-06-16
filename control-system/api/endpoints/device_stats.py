from typing import List, Sequence

from fastapi import APIRouter, Depends, Query

from core.dependencies.service import get_device_stats_service
from schemas.device_stats import (
    DeviceDailyAverageStats,
    DeviceHourlyAveragesStats,
    DeviceWeekdayAverageStats,
)
from services.device_stats import DeviceStatsService

router = APIRouter(prefix="/device_stats", tags=["Device Statistics"])


@router.get("/hourly_averages/", response_model=List[DeviceHourlyAveragesStats])
def get_hourly_averages(
    days: int = Query(30, ge=1),
    service: DeviceStatsService = Depends(get_device_stats_service),
):
    return service.get_hourly_averages(days)


@router.get("/weekday_averages/", response_model=List[DeviceWeekdayAverageStats])
def get_weekday_averages(
    weeks: int = Query(12, ge=1),
    service: DeviceStatsService = Depends(get_device_stats_service),
):
    return service.get_weekday_averages(weeks)


@router.get("/daily_averages/", response_model=Sequence[DeviceDailyAverageStats])
def get_daily_averages(
    months: int = Query(6, ge=1),
    service: DeviceStatsService = Depends(get_device_stats_service),
):
    return service.get_daily_averages(months)

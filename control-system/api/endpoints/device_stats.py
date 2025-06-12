from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.dependencies.db import get_db
from schemas.device_stats import DailyStats, HourlyStats, WeekdayStats
from services.device_stats import DeviceStatsService

router = APIRouter()


@router.get("/hourly_averages/", response_model=List[HourlyStats])
def get_hourly_averages(
    db: Session = Depends(get_db),
    days: int = Query(30, description="Количество дней для анализа", ge=1),
):
    return DeviceStatsService.get_hourly_averages(db, days)


@router.get("/weekday_averages/", response_model=List[WeekdayStats])
def get_weekday_averages(
    db: Session = Depends(get_db),
    weeks: int = Query(12, description="Количество недель для анализа", ge=1),
):
    return DeviceStatsService.get_weekday_averages(db, weeks)


@router.get("/daily_averages/", response_model=List[DailyStats])
def get_daily_averages(
    db: Session = Depends(get_db),
    months: int = Query(6, description="Количество месяцев для анализа", ge=1),
):
    return DeviceStatsService.get_daily_averages(db, months)

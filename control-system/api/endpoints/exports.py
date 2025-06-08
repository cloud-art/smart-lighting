from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.dependencies import get_db
from services.exports import ExportsService

router = APIRouter()


@router.get("/device_data_csv/")
def device_data_csv(
    db: Session = Depends(get_db),
    days: int = Query(30, description="Количество дней для анализа", ge=1),
):
    return ExportsService.export_device_data_csv(db, days)

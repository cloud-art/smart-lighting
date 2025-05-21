import calendar
from fastapi import FastAPI, Depends, Query, Request
from sqlalchemy.orm import Session, class_mapper
from database import SessionLocal, engine, Base
from models import DeviceData, DeviceDataCalculatedDim, DeviceDataCorrectedDim
from mqtt.client import mqtt_client
from sqlalchemy.future import select
from sqlalchemy import extract, func
from typing import List, Dict, Any
from datetime import datetime, timedelta
from urllib.parse import urlencode

app = FastAPI()

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup():
    create_tables()
    await mqtt_client.start()

def build_next_url(request: Request, page: int, page_size: int, total: int) -> str:
    if page * page_size >= total:
        return None
    params = dict(request.query_params)
    params['page'] = page + 1
    return f"{request.url.path}?{urlencode(params)}"

def model_to_dict(model_instance):
    if not model_instance:
        return None
    mapper = class_mapper(model_instance.__class__)
    columns = [column.key for column in mapper.columns]
    result = {}
    for column in columns:
        value = getattr(model_instance, column)
        if isinstance(value, datetime):
            value = value.isoformat()
        result[column] = value
    return result

@app.get("/api/device_data/", response_model=Dict[str, Any])
def get_device_data(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, description="Номер страницы", ge=1),
    page_size: int = Query(10, description="Количество записей на странице", ge=1, le=100)
):
    total_count = db.scalar(select(func.count()).select_from(DeviceData))
    offset = (page - 1) * page_size
    result = db.execute(select(DeviceData).offset(offset).limit(page_size))
    data = result.scalars().all()
    serialized_data = [model_to_dict(item) for item in data]
    next_url = build_next_url(request, page, page_size, total_count)
    
    return {
        "page": page,
        "next": next_url,
        "count": total_count,
        "result": serialized_data
    }

@app.get("/api/device_data_calculated_dim/", response_model=Dict[str, Any])
def get_device_data_calculated_dim(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, description="Номер страницы", ge=1),
    page_size: int = Query(10, description="Количество записей на странице", ge=1, le=100)
):
    total_count = db.scalar(select(func.count()).select_from(DeviceDataCalculatedDim))
    offset = (page - 1) * page_size
    result = db.execute(select(DeviceDataCalculatedDim).offset(offset).limit(page_size))
    data = result.scalars().all()
    serialized_data = [model_to_dict(item) for item in data]
    next_url = build_next_url(request, page, page_size, total_count)
    
    return {
        "page": page,
        "next": next_url,
        "count": total_count,
        "result": serialized_data
    }

@app.get("/api/device_data_summary/", response_model=Dict[str, Any])
def get_device_data_summary(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, description="Номер страницы", ge=1),
    page_size: int = Query(10, description="Количество записей на странице", ge=1, le=100)
):
    total_count = db.scalar(select(func.count()).select_from(DeviceData))
    offset = (page - 1) * page_size
    
    query = (
        select(
            DeviceData,
            DeviceDataCalculatedDim.dimming_level.label("calculated_dimming_level"),
            DeviceDataCorrectedDim.dimming_level.label("corrected_dimming_level")
        )
        .outerjoin(DeviceDataCalculatedDim, DeviceData.id == DeviceDataCalculatedDim.device_data_id)
        .outerjoin(DeviceDataCorrectedDim, DeviceData.id == DeviceDataCorrectedDim.device_data_id)
        .order_by(DeviceData.id)
        .offset(offset)
        .limit(page_size)
    )
    
    result = db.execute(query)
    data = result.all()
    
    serialized_data = []
    for row in data:
        device_data = model_to_dict(row.DeviceData)
        device_data["calculated_dimming_level"] = row.calculated_dimming_level
        device_data["corrected_dimming_level"] = row.corrected_dimming_level
        serialized_data.append(device_data)
    
    next_url = build_next_url(request, page, page_size, total_count)
    
    return {
        "page": page,
        "next": next_url,
        "count": total_count,
        "result": serialized_data
    }


@app.get("/api/stats/hourly_averages/")
def get_hourly_averages(
    db: Session = Depends(get_db),
    days: int = Query(30, description="Количество дней для анализа", ge=1)
) -> List[Dict[str, Any]]:
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    result = db.execute(
        select(
            extract('hour', DeviceData.timestamp).label("hour"),
            func.avg(DeviceData.car_count).label("avg_car_count"),
            func.avg(DeviceData.traffic_speed).label("avg_traffic_speed"),
            func.avg(DeviceData.pedestrian_count).label("avg_pedestrian_count"),
            func.avg(DeviceData.dimming_level).label("avg_dimming_level"),
            func.avg(DeviceDataCalculatedDim.dimming_level).label("avg_calculated_dim"),
            func.avg(DeviceDataCorrectedDim.dimming_level).label("avg_corrected_dim")
        )
        .outerjoin(DeviceDataCalculatedDim, DeviceData.id == DeviceDataCalculatedDim.device_data_id)
        .outerjoin(DeviceDataCorrectedDim, DeviceData.id == DeviceDataCorrectedDim.device_data_id)
        .where(DeviceData.timestamp.between(start_date, end_date))
        .group_by("hour")
        .order_by("hour")
    )
    
    return [{
        "hour": row.hour,
        "avg_car_count": float(row.avg_car_count) if row.avg_car_count is not None else None,
        "avg_traffic_speed": float(row.avg_traffic_speed) if row.avg_traffic_speed is not None else None,
        "avg_pedestrian_count": float(row.avg_pedestrian_count) if row.avg_pedestrian_count is not None else None,
        "avg_dimming_level": float(row.avg_dimming_level) if row.avg_dimming_level is not None else None,
        "avg_calculated_dim": float(row.avg_calculated_dim) if row.avg_calculated_dim is not None else None,
        "avg_corrected_dim": float(row.avg_corrected_dim) if row.avg_corrected_dim is not None else None
    } for row in result]

@app.get("/api/stats/weekday_averages/")
def get_weekday_averages(
    db: Session = Depends(get_db),
    weeks: int = Query(12, description="Количество недель для анализа", ge=1)
) -> List[Dict[str, Any]]:
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(weeks=weeks)
    
    result = db.execute(
        select(
            extract('dow', DeviceData.timestamp).label("weekday"),
            func.avg(DeviceData.car_count).label("avg_car_count"),
            func.avg(DeviceData.traffic_speed).label("avg_traffic_speed"),
            func.avg(DeviceData.pedestrian_count).label("avg_pedestrian_count"),
            func.avg(DeviceData.dimming_level).label("avg_dimming_level"),
            func.avg(DeviceDataCalculatedDim.dimming_level).label("avg_calculated_dim"),
            func.avg(DeviceDataCorrectedDim.dimming_level).label("avg_corrected_dim")
        )
        .outerjoin(DeviceDataCalculatedDim, DeviceData.id == DeviceDataCalculatedDim.device_data_id)
        .outerjoin(DeviceDataCorrectedDim, DeviceData.id == DeviceDataCorrectedDim.device_data_id)
        .where(DeviceData.timestamp.between(start_date, end_date))
        .group_by("weekday")
        .order_by("weekday")
    )
    
    weekday_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    return [{
        "weekday": int(row.weekday),
        "weekday_name": weekday_names[int(row.weekday)],
        "avg_car_count": float(row.avg_car_count) if row.avg_car_count is not None else None,
        "avg_traffic_speed": float(row.avg_traffic_speed) if row.avg_traffic_speed is not None else None,
        "avg_pedestrian_count": float(row.avg_pedestrian_count) if row.avg_pedestrian_count is not None else None,
        "avg_dimming_level": float(row.avg_dimming_level) if row.avg_dimming_level is not None else None,
        "avg_calculated_dim": float(row.avg_calculated_dim) if row.avg_calculated_dim is not None else None,
        "avg_corrected_dim": float(row.avg_corrected_dim) if row.avg_corrected_dim is not None else None
    } for row in result]

@app.get("/api/stats/daily_averages/")
def get_daily_averages(
    db: Session = Depends(get_db),
    months: int = Query(6, description="Количество месяцев для анализа", ge=1)
) -> List[Dict[str, Any]]:
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30*months)
    
    result = db.execute(
        select(
            extract('day', DeviceData.timestamp).label("day_of_month"),
            func.avg(DeviceData.car_count).label("avg_car_count"),
            func.avg(DeviceData.traffic_speed).label("avg_traffic_speed"),
            func.avg(DeviceData.pedestrian_count).label("avg_pedestrian_count"),
            func.avg(DeviceData.dimming_level).label("avg_dimming_level"),
            func.avg(DeviceDataCalculatedDim.dimming_level).label("avg_calculated_dim"),
            func.avg(DeviceDataCorrectedDim.dimming_level).label("avg_corrected_dim")
        )
        .outerjoin(DeviceDataCalculatedDim, DeviceData.id == DeviceDataCalculatedDim.device_data_id)
        .outerjoin(DeviceDataCorrectedDim, DeviceData.id == DeviceDataCorrectedDim.device_data_id)
        .where(DeviceData.timestamp.between(start_date, end_date))
        .group_by("day_of_month")
        .order_by("day_of_month")
    )
    
    return [{
        "day_of_month": int(row.day_of_month),
        "avg_car_count": float(row.avg_car_count) if row.avg_car_count is not None else None,
        "avg_traffic_speed": float(row.avg_traffic_speed) if row.avg_traffic_speed is not None else None,
        "avg_pedestrian_count": float(row.avg_pedestrian_count) if row.avg_pedestrian_count is not None else None,
        "avg_dimming_level": float(row.avg_dimming_level) if row.avg_dimming_level is not None else None,
        "avg_calculated_dim": float(row.avg_calculated_dim) if row.avg_calculated_dim is not None else None,
        "avg_corrected_dim": float(row.avg_corrected_dim) if row.avg_corrected_dim is not None else None
    } for row in result]
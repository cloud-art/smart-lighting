from typing import Any, Dict

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.device import Device
from schemas.device import DeviceDBItem
from utils.pagination import build_next_url


class DeviceService:
    @staticmethod
    def get_device_data(
        db: Session, request: Any, page: int = 1, page_size: int = 10
    ) -> Dict[str, Any]:
        total_count = db.scalar(select(func.count()).select_from(Device))
        offset = (page - 1) * page_size
        result = db.execute(select(Device).offset(offset).limit(page_size))
        data = result.scalars().all()
        serialized_data = [DeviceDBItem(item) for item in data]
        next_url = build_next_url(request, page, page_size, total_count)

        return {
            "page": page,
            "next": next_url,
            "count": total_count,
            "results": serialized_data,
        }

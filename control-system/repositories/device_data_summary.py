from typing import Any, Optional, Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.device_data import DeviceDataModel
from models.device_data_calculated_dim import DeviceDataCalculatedDimModel
from models.device_data_corrected_dim import DeviceDataCorrectedDimModel
from repositories.base import QueryBuilder
from schemas.device_data import (
    DeviceDataSummaryUpdateSchema,
)


class DeviceDataSummaryRepository:
    def __init__(self, db: Session):
        self.db = db
        self.query_builder = QueryBuilder(DeviceDataModel)

    def _select(self):
        return (
            select(DeviceDataModel)
            .outerjoin(
                DeviceDataCalculatedDimModel,
                DeviceDataModel.id == DeviceDataCalculatedDimModel.device_data_id,
            )
            .outerjoin(
                DeviceDataCorrectedDimModel,
                DeviceDataModel.id == DeviceDataCorrectedDimModel.device_data_id,
            )
        )

    def get_by_id(self, id: int):
        query = self._select().filter(DeviceDataModel.id == id)
        result = self.db.execute(query)
        db_item = result.scalars().first()
        return db_item

    def get_all(self, page: int, page_size: int, device_id: Optional[int] = None):
        offset = (page - 1) * page_size
        query = self._select()
        if device_id is not None:
            query = query.filter(DeviceDataModel.device_id == device_id)
        query = query.order_by(DeviceDataModel.id).offset(offset).limit(page_size)

        result = self.db.execute(query).scalars().all()
        return result

    def get_total_count(self, device_id: Optional[int] = None):
        query = select(func.count()).select_from(DeviceDataModel)
        if device_id:
            query = query.where(DeviceDataModel.device_id == device_id)

        return self.db.scalar(select(func.count()).select_from(DeviceDataModel))

    def create(self, data: Any):
        return super().create(data)

    def update(self, id: int, data: DeviceDataSummaryUpdateSchema):
        summary_item = self.get_by_id(id)
        if not summary_item:
            return None
        
        corrected_dim = summary_item.corrected_dimming_level

        if corrected_dim:
            corrected_dim.dimming_level = data.corrected_dimming_level
        else:
            corrected_dim = DeviceDataCorrectedDimModel(
                device_data_id=id, dimming_level=data.corrected_dimming_level
            )
            self.db.add(corrected_dim)

        self.db.commit()
        self.db.refresh(corrected_dim)
        self.db.refresh(summary_item)

        return summary_item

    def bulk_update(self, ids: Sequence[int], data: DeviceDataSummaryUpdateSchema):
        success_count = 0

        for id in ids:
            summary_item = self.get_by_id(id)
            if not summary_item:
                break
            corrected_dim = summary_item.corrected_dimming_level

            if corrected_dim:
                corrected_dim.dimming_level = data.corrected_dimming_level
            else:
                corrected_dim = DeviceDataCorrectedDimModel(
                    device_data_id=id, dimming_level=data.corrected_dimming_level
                )
                self.db.add(corrected_dim)

            success_count += 1

        self.db.commit()

        return success_count

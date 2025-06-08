from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.device_data import DeviceData, DeviceDataCorrectedDim, DeviceDataModel
from models.device_data_calculated_dim import DeviceDataCalculatedDimModel
from models.device_data_corrected_dim import DeviceDataCorrectedDimModel
from schemas.device_data import DeviceDataSchema, DeviceDataSummarySchema
from schemas.device_data_dim_info import DeviceDataDimInfoDBItem


class DeviceDataSummaryRepository:
    def __init__(self, db: Session):
        self.db = db

    def update_summary_corrected_dim(
        self, device_data_id: int, dimming_level: float
    ) -> DeviceDataDimInfoDBItem:
        corrected_dim = self.db.get(DeviceDataCorrectedDimModel, device_data_id)

        if corrected_dim:
            corrected_dim.dimming_level = dimming_level
        else:
            corrected_dim = DeviceDataCorrectedDimModel(
                device_data_id=device_data_id, dimming_level=dimming_level
            )
            self.db.add(corrected_dim)

        self.db.commit()
        self.db.refresh(corrected_dim)
        return DeviceDataDimInfoDBItem.model_validate(corrected_dim)

    def get_summary_paginated_data(
        self, page: int, page_size: int
    ) -> List[DeviceDataSummarySchema]:
        offset = (page - 1) * page_size
        query = (
            select(
                DeviceDataModel,
                DeviceDataCalculatedDimModel.dimming_level.label(
                    "calculated_dimming_level"
                ),
                DeviceDataCorrectedDimModel.dimming_level.label(
                    "corrected_dimming_level"
                ),
            )
            .outerjoin(
                DeviceDataCalculatedDimModel,
                DeviceDataModel.id == DeviceDataCalculatedDimModel.device_data_id,
            )
            .outerjoin(
                DeviceDataCorrectedDimModel,
                DeviceDataModel.id == DeviceDataCorrectedDimModel.device_data_id,
            )
            .order_by(DeviceDataModel.id)
            .offset(offset)
            .limit(page_size)
        )
        result = self.db.execute(query).all()
        return [DeviceDataSummarySchema.model_validate(item) for item in result]

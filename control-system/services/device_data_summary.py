from typing import Any, Dict, List

from fastapi import HTTPException, status

from repositories.device_data import DeviceDataRepository
from repositories.device_data_summary import DeviceDataSummaryRepository
from schemas.base import PaginatedResponse
from schemas.device_data import DeviceDataSummarySchema
from schemas.device_data_dim_info import DeviceDataDimInfoSchema
from utils.pagination import Pagination


class DeviceDataSummaryService:
    def __init__(
        self,
        db_repo: DeviceDataRepository,
        db_summary_repo: DeviceDataSummaryRepository,
    ):
        self.db_repo = db_repo
        self.db_summary_repo = db_summary_repo

    def get_device_summary_data(
        self, request: Any, page: int = 1, page_size: int = 10
    ) -> PaginatedResponse[DeviceDataSummarySchema]:
        data = self.db_summary_repo.get_summary_paginated_data(page, page_size)
        total_count = self.db_repo.get_total_count()

        return Pagination.paginate(
            request=request,
            items=[DeviceDataSummarySchema.model_validate(row) for row in data],
            page=page,
            page_size=page_size,
            total_count=total_count,
        )

    def update_device_summary_dim(
        self, device_data_id: int, dimming_level: float
    ) -> Dict[str, Any]:
        self._validate_dimming_level(dimming_level)

        if not self.db_repo.get_by_id(device_data_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Device data not found"
            )

        corrected_dim = self.db_summary_repo.update_summary_corrected_dim(
            device_data_id, dimming_level
        )

        return {
            "success": True,
            "device_data_id": device_data_id,
            "corrected_dimming_level": corrected_dim.dimming_level,
        }

    def bulk_device_summary_update(
        self, updates: List[DeviceDataDimInfoSchema]
    ) -> Dict[str, Any]:
        results = {"success": [], "errors": []}

        for update in updates:
            try:
                self._validate_update(update)
                corrected_dim = self.db_summary_repo.update_summary_corrected_dim(
                    update.device_data_id, update.dimming_level
                )
                results["success"].append(
                    {
                        "device_data_id": corrected_dim.device_data_id,
                        "corrected_dimming_level": corrected_dim.dimming_level,
                    }
                )
            except Exception as e:
                self.db_repo.db.rollback()
                results["errors"].append(
                    {"device_data_id": update.device_data_id, "error": str(e)}
                )

        return {
            "total_requests": len(updates),
            "successful_updates": len(results["success"]),
            "failed_updates": len(results["errors"]),
            "details": results,
        }

    def _validate_dimming_level(self, dimming_level: float):
        if not isinstance(dimming_level, (int, float)) or not (
            0 <= dimming_level <= 100
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="corrected_dimming_level must be a number between 0 and 100",
            )

    def _validate_update(self, update: Dict[str, Any]):
        if None in (
            update.get("device_data_id"),
            update.get("corrected_dimming_level"),
        ):
            raise ValueError("Missing required fields")

        if (
            not isinstance(update["device_data_id"], int)
            or update["device_data_id"] <= 0
        ):
            raise ValueError("device_data_id must be a positive integer")

        self._validate_dimming_level(update["corrected_dimming_level"])

from fastapi import APIRouter

from api.endpoints import (
    device,
    device_data,
    device_data_calculated_dim,
    device_data_corrected_dim,
    device_data_summary,
    device_stats,
)

router = APIRouter()
router.include_router(device.router)
router.include_router(device_data.router)
router.include_router(device_data_summary.router)
router.include_router(device_data_calculated_dim.router)
router.include_router(device_data_corrected_dim.router)
router.include_router(device_stats.router)

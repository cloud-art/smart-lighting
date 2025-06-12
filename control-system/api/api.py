from fastapi import APIRouter

from api.endpoints import device, device_data

# , device_stats, exports

router = APIRouter()
router.include_router(device_data.router, prefix="/device_data", tags=["Device Data"])
# router.include_router(
#     device_stats.router, prefix="/device_stats", tags=["Device Statistics"]
# )
router.include_router(device.router, prefix="/device", tags=["Device"])
# router.include_router(exports.router, prefix="/exports", tags=["Exports"])

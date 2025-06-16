from typing import Callable, Literal, Optional

from fastapi import APIRouter, Body, Depends, Request
from pydantic import BaseModel

from schemas.base import PaginatedResponse
from schemas.pagination import PaginationParams
from services.base import BaseCRUDService

AllowedRoutes = Literal[
    "get_all_paginated", "get_by_id", "create", "update", "bulk_update", "delete"
]


class BulkUpdateSchema(BaseModel):
    ids: list[int]


class CRUDRouter[
    InstanceSchema: BaseModel,
    CreateSchema: Optional[BaseModel],
    UpdateSchema: Optional[BaseModel],
]:
    def __init__(
        self,
        service_factory: Callable[..., BaseCRUDService[InstanceSchema]],
        prefix: str,
        tags: list[str],
        allowed_routes: list[AllowedRoutes],
    ):
        self.router = APIRouter(prefix=prefix, tags=tags)
        self.service_factory = service_factory
        self.allowed_routes = allowed_routes
        self._setup_routes()

    def setup_get_all_paginated(self):
        @self.router.get("/", response_model=PaginatedResponse[InstanceSchema])
        async def get_all(
            request: Request,
            pagination: PaginationParams = Depends(),
            service: BaseCRUDService[InstanceSchema] = Depends(self.service_factory),
        ):
            return service.get_all_paginated(
                request, pagination.page, pagination.page_size
            )

    def setup_get_by_id(self):
        @self.router.get("/{item_id}", response_model=InstanceSchema)
        async def get_by_id(
            item_id: int,
            service: BaseCRUDService[InstanceSchema] = Depends(self.service_factory),
        ):
            return service.get_by_id(item_id)

    def setup_create(self):
        @self.router.post("/", response_model=InstanceSchema)
        async def create(
            item: CreateSchema,
            service: BaseCRUDService[InstanceSchema] = Depends(self.service_factory),
        ):
            return service.create(item)

    def setup_update(self):
        @self.router.put("/{item_id}", response_model=InstanceSchema)
        async def update(
            item_id: int,
            item: InstanceSchema,
            service: BaseCRUDService[InstanceSchema] = Depends(self.service_factory),
        ):
            return service.update(item_id, item)

    def setup_bulk_update(self):
        @self.router.post("/bulk_update", response_model=int)
        async def update(
            body: BulkUpdateSchema = Body(),
            service: BaseCRUDService[InstanceSchema] = Depends(self.service_factory),
        ):
            update_data = UpdateSchema(**body.model_dump(exclude={"ids"}))
            return service.update(body.ids, update_data)

    def setup_delete(self):
        @self.router.delete("/{item_id}")
        async def delete(item_id: int):
            raise NotImplementedError("Delete method not implemented")

    def _setup_routes(self):
        if "get_all_paginated" in self.allowed_routes:
            self.setup_get_all_paginated()

        if "get_by_id" in self.allowed_routes:
            self.setup_get_by_id()

        if "create" in self.allowed_routes:
            self.setup_create()

        if "update" in self.allowed_routes:
            self.setup_update()

        if "bulk_update" in self.allowed_routes:
            self.setup_bulk_update()

        if "delete" in self.allowed_routes:
            self.setup_delete()

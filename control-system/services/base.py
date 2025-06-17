from typing import Any, Dict, List, Optional, Sequence, Tuple

from fastapi import HTTPException, Request, status
from pydantic import BaseModel

from core import logger
from repositories.base import BaseCRUDRepository
from schemas.base import PaginatedResponse
from utils.pagination import Pagination


class BaseCRUDServiceSchema(BaseModel):
    class Config:
        from_attributes = True


class BaseCRUDService[InstanceSchemaType: BaseCRUDServiceSchema]:
    def __init__(
        self, repository: BaseCRUDRepository, instance_schema: InstanceSchemaType
    ):
        self.repository = repository
        self.instance_schema = instance_schema

    def create(self, data: BaseModel) -> InstanceSchemaType:
        data = self.repository.create(data)
        logger.logger.info(data)
        return self.instance_schema.model_validate(data)

    def update(self, item_id: int, data: BaseModel) -> InstanceSchemaType:
        data = self.repository.update(item_id, data)
        return self.instance_schema.model_validate(data)

    def bulk_update(self, item_ids: Sequence[int], data: BaseModel) -> int:
        return self.repository.bulk_update(item_ids, data)

    def get_by_id(
        self,
        item_id: int,
        filters: Optional[Dict[str, Any]] = None,
        joins: Optional[List[Tuple[str, Any]]] = None,
    ) -> InstanceSchemaType:
        data = self.repository.get_one(
            filters={"id": item_id, **(filters or {})}, joins=joins
        )
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object with id {item_id} not found",
            )
        return self.instance_schema.model_validate(data)

    def get_all(
        self,
        request: Request,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None,
        joins: Optional[List[Tuple[str, Any]]] = None,
        order_by: Optional[Dict[str, Any]] = None,
    ) -> PaginatedResponse[InstanceSchemaType]:
        offset = (page - 1) * page_size
        logger.logger.info(joins)
        total_count = self.get_total_count(filters=filters, joins=joins)
        data = self.repository.get_all(
            filters=filters,
            joins=joins,
            order_by=order_by,
            offset=offset,
            limit=page_size,
        )
        return Pagination[InstanceSchemaType].paginate(
            request=request,
            items=[self.instance_schema.model_validate(item) for item in data],
            page=page,
            page_size=page_size,
            total_count=total_count,
        )

    def get_total_count(
        self,
        filters: Dict[str, Any] | None = None,
        joins: Optional[List[Tuple[str, Any]]] = None,
    ) -> int:
        logger.logger.info(joins)
        return self.repository.get_total_count(filters=filters, joins=joins)

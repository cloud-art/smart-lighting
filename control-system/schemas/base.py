from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginatedResponse(GenericModel, Generic[T]):
    page: int
    next: Optional[str]
    count: int
    results: list[T]


class BulkUpdateSchema(BaseModel):
    ids: list[int]

from typing import Any
from urllib.parse import urlencode

from schemas.base import PaginatedResponse


class Pagination[T]:
    @staticmethod
    def paginate(
        request: Any, items: list[T], page: int, page_size: int, total_count: int
    ) -> PaginatedResponse[T]:
        next_url = Pagination.build_next_url(request, page, page_size, total_count)

        return PaginatedResponse[T](
            page=page, next=next_url, count=total_count, results=items
        )

    @staticmethod
    def build_next_url(
        request: Any, page: int, page_size: int, total: int
    ) -> str | None:
        if page * page_size >= total:
            return None
        params = dict(request.query_params)
        params["page"] = page + 1
        return f"{request.url.path}?{urlencode(params)}"

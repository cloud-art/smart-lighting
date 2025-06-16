from fastapi import Query


class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, description="Номер страницы", ge=1),
        page_size: int = Query(
            10, description="Количество записей на странице", ge=1, le=100
        ),
    ):
        self.page = page
        self.page_size = page_size

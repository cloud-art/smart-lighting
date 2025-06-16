from abc import ABC, abstractmethod
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    Type,
    Union,
    runtime_checkable,
)

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import Select, and_, func, select, update
from sqlalchemy.orm import DeclarativeBase, Session, aliased

from core import logger


class Base(DeclarativeBase):
    pass


@runtime_checkable
class HasIdProtocol(Protocol):
    id: Any


class Repository(ABC):
    def __init__(self, db: Session):
        self.db = db

    @abstractmethod
    def get_one(
        self, filters: Dict[str, Any], joins: Optional[List[Tuple[str, Any]]] = None
    ) -> Any:
        raise NotImplementedError("Get by id operation is not allowed")

    @abstractmethod
    def get_all(
        self,
        *,
        filters: Optional[Dict[str, Any]] = None,
        joins: Optional[List[Tuple[str, Any]]] = None,
        order_by: Optional[Union[str, List[str]]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[Any]:
        raise NotImplementedError("Get all operation is not allowed")

    @abstractmethod
    def get_total_count(
        self,
        filters: Optional[Dict[str, Any]] = None,
        joins: Optional[List[Tuple[str, Any]]] = None,
    ) -> int:
        raise NotImplementedError("Get total count operation is not allowed")


class CRUDRepository(Repository):
    def __init__(self, db: Session):
        super().__init__(db)

    @abstractmethod
    def create(self, data: Any) -> Any:
        raise NotImplementedError("Create operation is not allowed")

    @abstractmethod
    def update(self, id: int, data: Any) -> Optional[Any]:
        raise NotImplementedError("Update operation is not allowed")

    @abstractmethod
    def bulk_update(self, ids: Sequence[int], data: Any) -> int:
        raise NotImplementedError("Bulk update operation is not allowed")


class QueryBuilder:
    def __init__(self, model: Base):
        self.model = model

    def build_filter_conditions(
        self, filters: Dict[str, Any], joins: Optional[List[Tuple[str, Any]]] = None
    ) -> Any:
        conditions = []
        join_aliases = {}

        if joins:
            for relation_name, model in joins:
                join_aliases[relation_name] = aliased(model)

        for key, value in filters.items():
            parts = key.split("__")

            current_model = self.model
            field_path = []
            operators = []

            for part in parts:
                if part in [
                    "eq",
                    "ne",
                    "gt",
                    "lt",
                    "gte",
                    "lte",
                    "in",
                    "like",
                    "ilike",
                    "is_null",
                ]:
                    operators.append(part)
                else:
                    field_path.append(part)

            operator = operators[-1] if operators else "eq"

            field = None
            for i, field_name in enumerate(field_path):
                if i < len(field_path) - 1:
                    rel = getattr(current_model, field_name, None)
                    if rel is None:
                        raise ValueError(f"Relation '{field_name}' not found in model")
                    current_model = rel.mapper.class_
                else:
                    field = getattr(current_model, field_name, None)
                    if field is None:
                        raise ValueError(f"Field '{field_name}' not found in model")

            if isinstance(value, (int, float)):
                value = (
                    float(value)
                    if isinstance(field.type, sqlalchemy.Float)
                    else int(value)
                )

            if operator == "eq":
                conditions.append(field == value)
            elif operator == "ne":
                conditions.append(field != value)
            elif operator == "gt":
                conditions.append(field > value)
            elif operator == "lt":
                conditions.append(field < value)
            elif operator == "gte":
                conditions.append(field >= value)
            elif operator == "lte":
                conditions.append(field <= value)
            elif operator == "in":
                conditions.append(field.in_(value))
            elif operator == "like":
                conditions.append(field.like(value))
            elif operator == "ilike":
                conditions.append(field.ilike(value))
            elif operator == "is_null":
                if value:
                    conditions.append(field.is_(None))
                else:
                    conditions.append(field.is_not(None))
            else:
                raise ValueError(f"Unknown operator '{operator}'")

        return and_(*conditions) if conditions else True

    def apply_ordering(self, query: Select, order_by: Union[str, List[str]]) -> Any:
        if isinstance(order_by, str):
            order_by = [order_by]

        order_clauses = []

        for field in order_by:
            direction = "asc"
            if field.startswith("-"):
                direction = "desc"
                field = field[1:]

            model_field = getattr(self.model, field, None)
            if model_field is None:
                raise ValueError(f"Field '{field}' not found in model")

            if direction == "asc":
                order_clauses.append(model_field.asc())
            else:
                order_clauses.append(model_field.desc())

        return query.order_by(*order_clauses)


class BaseCRUDRepository[
    ModelType: (Base, HasIdProtocol),
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
](CRUDRepository):
    def __init__(self, db: Session, model: Type[ModelType]):
        super().__init__(db)
        self.model = model
        self.query_builder = QueryBuilder(model)

    def create(self, data: CreateSchemaType) -> ModelType:
        db_item = self.model(**data.model_dump())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update(self, item_id: int, data: UpdateSchemaType) -> Optional[ModelType]:
        db_item = self.get_one(filters={"id": item_id})
        if db_item:
            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(db_item, key, value)
            self.db.commit()
            self.db.refresh(db_item)
            return db_item
        return None

    def bulk_update(self, item_ids: Sequence[int], data: UpdateSchemaType) -> int:
        update_data = data.model_dump(exclude_unset=True)
        result = self.db.execute(
            update(self.model).where(self.model.id.in_(item_ids)).values(**update_data)
        )
        self.db.commit()
        return result.rowcount

    def get_all(
        self,
        *,
        filters: Optional[Dict[str, Any]] = None,
        joins: Optional[List[Tuple[str, Any]]] = None,
        order_by: Optional[Union[str, List[str]]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[ModelType]:
        query = select(self.model)
        logger.logger.warning(joins)
        if joins:
            for relation_name, _ in joins:
                query = query.join(getattr(self.model, relation_name))

        if filters:
            query = query.where(
                self.query_builder.build_filter_conditions(filters, joins=joins)
            )

        if order_by:
            query = self.query_builder.apply_ordering(query, order_by)

        if offset is not None:
            query = query.offset(offset)

        if limit is not None:
            query = query.limit(limit)

        result = self.db.execute(query)
        return result.scalars().all()

    def get_one(
        self, filters: Dict[str, Any], joins: Optional[List[Tuple[str, Any]]] = None
    ) -> Optional[ModelType]:
        query = select(self.model)
        if joins:
            for relation_name, _ in joins:
                query = query.join(getattr(self.model, relation_name))

        query = query.where(
            self.query_builder.build_filter_conditions(filters=filters, joins=joins)
        ).limit(1)
        result = self.db.execute(query)
        return result.scalars().first()

    def get_total_count(
        self,
        filters: Optional[Dict[str, Any]] = None,
        joins: Optional[List[Tuple[str, Any]]] = None,
    ) -> int:
        query = select(func.count()).select_from(self.model)

        if joins:
            for relation_name, _ in joins:
                query = query.join(getattr(self.model, relation_name))

        if filters:
            query = query.where(
                self.query_builder.build_filter_conditions(filters, joins=joins)
            )

        return self.db.scalar(query)

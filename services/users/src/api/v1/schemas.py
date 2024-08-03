import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel

TData = TypeVar("TData")
TListItem = TypeVar("TListItem")


class PaginationOutSchema(BaseModel):
    limit: int
    offset: int
    total: int


class PaginationQuery(BaseModel):
    limit: int
    offset: int


@dataclass
class ListPaginatedResponse(Generic[TListItem]):
    items: list[TListItem]
    pagination: PaginationOutSchema


@dataclass
class UserOut:
    id: uuid.UUID
    username: str
    email: str
    is_active: bool
    is_verified: bool
    is_superuser: bool


@dataclass
class APIResponse(Generic[TData]):
    ok: bool
    data: TData | dict | list = field(default_factory=dict)


@dataclass
class ErrorAPIResponse:
    ok: bool
    error_code: int
    detail: str

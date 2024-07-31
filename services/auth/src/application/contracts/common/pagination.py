from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import BaseModel

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

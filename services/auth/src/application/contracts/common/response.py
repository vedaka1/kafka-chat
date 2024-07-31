from dataclasses import dataclass, field
from typing import Generic, TypeVar

TData = TypeVar("TData")


@dataclass
class APIResponse(Generic[TData]):
    ok: bool
    data: TData | dict | list = field(default_factory=dict)


@dataclass
class ErrorAPIResponse:
    ok: bool
    error_code: int
    details: str

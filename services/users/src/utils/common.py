import os
from typing import Any


def cache_result(func):
    cache = {}

    async def wrapper(*args, **kwargs):
        key = func.__name__
        if key in cache:
            return cache[key]
        result = await func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper


def get_env_var(key: str, to_cast: Any, default: Any | None = None) -> Any:
    """
    Converting environment variable types
    Args:
        key (str): environment variable
        to_cast (Any): type to convert
        default (Any, optional): default value
    Raises:
        RuntimeError: occurs if such a variable is not found in .env
    Returns:
        Any: an environment variable with a converted type
    """
    value = os.getenv(key)

    if not value and not default:
        raise RuntimeError(f"{key} environment variable not set")
    if not value:
        return default
    return to_cast(value)

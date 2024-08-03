def cache_async_result(func):
    cache = {}

    async def wrapper(*args, **kwargs):
        key = func.__name__
        if key in cache:
            return cache[key]
        result = await func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper

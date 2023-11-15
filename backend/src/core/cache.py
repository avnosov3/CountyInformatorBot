import pickle
from functools import wraps
from typing import Any, Callable

from django.core.cache import caches

from core.settings import CACHE_ENABLE


def cache_handler(cache_name: str, expire: int | None = None) -> Callable[[Any], Any]:
    """Декоратор для кеширования."""

    def decorator(func: Callable) -> Callable[[Any], Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            if not CACHE_ENABLE:
                return await func(*args, **kwargs)
            cache = caches[cache_name]
            hashed_args_kwargs = hash(f"{args}{kwargs}")

            timeout = cache.default_timeout if expire is None else expire
            key = f"{cache_name}:{hashed_args_kwargs}"

            item = await cache.aget(key)
            if item:
                return pickle.loads(item)

            result = await func(*args, **kwargs)
            if result:
                await cache.aset(key=key, value=pickle.dumps(result), timeout=timeout)

            return result

        return wrapper

    return decorator

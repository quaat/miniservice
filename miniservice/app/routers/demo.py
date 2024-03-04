from fastapi import APIRouter, Depends
from typing import AsyncGenerator, Dict
from redis.asyncio import Redis, from_url
from core.models.person import Person
from core.modules.cacheservice import CacheService


# Factory function for cache backend
async def get_redis_cache() -> AsyncGenerator[Redis, None]:
    """
    Asynchronous generator that provides a Redis connection.

    Establishes and yields a Redis connection, ensuring the connection is closed after use.
    """
    redis = await from_url("redis://redis:6379")
    try:
        yield redis
    finally:
        await redis.aclose()

# Factory function for cache service with dependency injection
async def get_cache_service(cache: Redis = Depends(get_redis_cache)) -> CacheService:
    """
    Dependency that provides a CacheService instance.
    """
    return CacheService(cache)


router = APIRouter(prefix="/person")

@router.post(
    "/populate/",
    summary="Populate Redis with a Person object",
    response_description="The hash key of the stored Person object",
)


async def store_person(
    person: Person, service: CacheService = Depends(get_cache_service)
) -> Dict[str, str]:
    """
    Endpoint to serialize and store a Person object in Redis.
    """
    hash_key = await service.store_person(person)
    return {"hash": hash_key}


@router.get(
    "/retrieve/{hash_key}",
    summary="Retrieve a Person object from Redis",
    response_model=Person,
    response_description="The retrieved Person object",
)
async def retrieve_person(
    hash_key: str, service: CacheService = Depends(get_cache_service)
) -> Person:
    """
    Endpoint to retrieve a Person object from Redis using a SHA1 hash key.
    """
    return await service.retrieve_person(hash_key)

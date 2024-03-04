import hashlib
from redis.asyncio import Redis, from_url
from core.models.person import Person
from fastapi import HTTPException, Depends
from typing import AsyncGenerator
import json


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


class CacheService:
    """
    A service for caching and retrieving Person objects in Redis.
    """

    def __init__(self, cache: Redis):
        self.cache = cache

    async def store_person(self, person: Person) -> str:
        """
        Serializes a Person object and stores it in Redis, keyed by a SHA1 hash of the serialized data.

        Args:
            person (Person): The person object to serialize and store.

        Returns:
            str: The SHA1 hash key under which the person object was stored.
        """
        person_json = person.model_dump_json().encode("utf-8")
        person_hash = hashlib.sha1(person_json).hexdigest()
        await self.cache.set(person_hash, person_json)
        return person_hash

    async def retrieve_person(self, hash_key: str) -> Person:
        """
        Retrieves a Person object from Redis using the specified SHA1 hash key.

        Args:
            hash_key (str): The SHA1 hash key of the person object to retrieve.

        Returns:
            Person: The deserialized person object.

        Raises:
            HTTPException: If the person object does not exist in Redis.
        """
        result = await self.cache.get(hash_key)
        if not result:
            raise HTTPException(status_code=404, detail="Person not found")
        person_dict = json.loads(result.decode("utf-8"))
        return Person(**person_dict)


async def get_cache_service(cache: Redis = Depends(get_redis_cache)) -> CacheService:
    """
    Dependency that provides a CacheService instance.
    """
    return CacheService(cache)
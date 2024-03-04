import hashlib
from core.models.person import Person
from fastapi import HTTPException
from typing import Any, Protocol, runtime_checkable
import json

@runtime_checkable
class ICacheBackend(Protocol):
    async def set(self, key: str, value: Any) -> None:
        ...

    async def get(self, key: str) -> Any:
        ...

    async def aclose(self):
        ...

class CacheService:
    """
    A service for caching and retrieving Person objects in Redis.
    """

    def __init__(self, cache: ICacheBackend):
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

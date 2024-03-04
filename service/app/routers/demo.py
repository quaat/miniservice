from fastapi import APIRouter, Depends
from typing import Dict
from core.models.person import Person
from core.modules.cacheservice import CacheService, get_cache_service

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

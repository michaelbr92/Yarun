from enum import Enum
from functools import reduce
from typing import List, Union
from fastapi import APIRouter, Response, HTTPException
from minio.datatypes import Bucket
from connections import minio_client
from structs import File

router = APIRouter(prefix='/bucket')


class Bucket:
    def __init__(bucket_name):
        pass

    @property
    def tags() -> List[str]:
        pass


@router.get("/list", response_model=List[str])
async def list_buckets() -> List[str]:
    buckets = minio_client.list_buckets()  # type: List[Bucket]
    return list(map(lambda bucket: bucket.name, buckets))


@router.get("/{bucket_name}/tags", response_model=List[str])
async def get_tags(bucket_name: str) -> List[str]:
    objects = minio_client.list_objects(bucket_name, recursive=True)
    tags = map(lambda obj: minio_client.get_object_tags(
        bucket_name, obj.object_name), objects)
    tags = (x.keys() for x in tags if x is not None)
    return list(set(reduce(lambda x, y: x+list(y), tags, [])))


@router.get("/{bucket_name}/tag/{tag_name}", response_model=List[str])
async def get_tag_options(bucket_name: str, tag_name: str) -> List[str]:

    if tag_name not in await get_tags(bucket_name=bucket_name):
        raise HTTPException(status_code=404, detail="No such tag")

    objects = minio_client.list_objects(bucket_name, recursive=True)
    tags = map(lambda obj: minio_client.get_object_tags(
        bucket_name, obj.object_name), objects)
    types = (x.get(tag_name, None) for x in tags if x is not None)
    return list(set(filter(lambda x: x is not None, types)))


@router.get("/{bucket_name}/files", response_model=List[File])
async def get_files(bucket_name: str, tagKey: Union[str, None] = None, tagValue: Union[str, None] = None) -> List[File]:
    """
    Get files of bucket 

    :param bucket_name: The name the bucket to search in  
    :param tag: Tags to filter with, defaults to None  
    :return: List of Files  
    """
    objects = minio_client.list_objects(bucket_name, recursive=True)

    # Chekc tag has key and value
    if sum([val is not None for val in [tagValue, tagKey]]) == 1:
        raise HTTPException(
            status_code=400, detail="Tag should have key and value")

    # Add filter of tags to object
    if tagKey is not None and tagValue is not None:
        objects = filter(
            lambda obj: (minio_client.get_object_tags(
                bucket_name, obj.object_name) or {}).get(tagKey, None) == tagValue,
            objects
        )

    return [
        File(
            bucket=bucket_name,
            name=obj.object_name,
        )
        for obj in objects]


from typing import Any, Union
import celery
from fastapi import APIRouter, Body
from fastapi.exceptions import HTTPException

from tasks.rules import run_rule_on_object, is_rule_valid
from structs import File, TaskStatus, TaskResult, RuleString, RuleResult
from connections import minio_client
from celery.result import AsyncResult

router = APIRouter(prefix='/task')


@router.post("/validate")
async def task_enque(signature: str = Body(embed=True)) -> str:
    task = is_rule_valid.delay(signature)
    try:
        return task.get(timeout=3)
    except celery.exceptions.TimeoutError:
        raise HTTPException(status_code=504, detail="Validation timed out")


@router.post("/new")
async def task_enque(file: File = Body(embed=True), signature: str = Body(embed=True)) -> str:
    # raw_data_resp = minio_client.get_object(
    # bucket_name=file.bucket,
    # object_name=file.name
    # )
    # raw_data = raw_data_resp.data
    new_task = run_rule_on_object.delay(
        raw_rule=signature, bucket_name=file.bucket, object_name=file.name)
    return new_task.id


@router.get("/{uid}/status", response_model=TaskStatus)
async def task_status(uid: str) -> TaskStatus:
    task_result = AsyncResult(uid)
    return task_result.status


@router.get("/{uid}/result", response_model=Union[TaskResult, Any])
async def task_result(uid: str) -> TaskResult:
    task_result = AsyncResult(uid)
    task_status = task_result.status
    if not task_status == TaskStatus.SUCCESS:
        return TaskResult(status=task_status)
    raw_result = task_result.get()
    result = TaskResult(
        status=task_status,
        file=File(
            bucket=raw_result["file"]["bucket"],
            name=raw_result["file"]["name"]
        ),
        rule=RuleResult(
            matches=raw_result["result"]["matches"],
            name=raw_result["result"]["rule"],
            tags=raw_result["result"]["tags"],
            console=raw_result["console"],
            strings=[
                RuleString(
                    offset=s[0],
                    name=s[1],
                    hex_result=s[2]
                )
                for s in raw_result["result"]["strings"]
            ]
        )
    )
    return result

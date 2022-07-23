from enum import Enum
import json
from typing import Any, List, Union
from pydantic import BaseModel


class File(BaseModel):
    bucket: str
    name: str


class TaskStatus(str, Enum):
    PENDING = 'PENDING'
    STARTED = 'STARTED'
    RETRY = 'RETRY'
    FAILURE = 'FAILURE'
    SUCCESS = 'SUCCESS'


class RuleString(BaseModel):
    offset: int
    name: str
    hex_result: str


class RuleResult(BaseModel):
    matches: bool
    name: str
    console: List[str]
    tags: List[str]
    strings: List[RuleString]


class TaskResult(BaseModel):
    status: TaskStatus
    file: File
    rule: Union[RuleResult, None]

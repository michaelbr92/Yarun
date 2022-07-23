import time
from os import environ

import yara
from celery import Celery, current_task
from minio import Minio
from connections import minio_client, celery_app


def get_file(bucket_name: str, object_name: str) -> bytes:
    return minio_client.get_object(bucket_name=bucket_name, object_name=object_name).data


@celery_app.task(name="tasks.add")
def add(x, y):
    # print(current_task)
    # time.sleep(5)
    return x + y


@celery_app.task(name="tasks.run_rule_on_object")
def run_rule_on_object(raw_rule: str, bucket_name: str, object_name: str):
    data = get_file(bucket_name=bucket_name, object_name=object_name)
    rule = yara.compile(source=raw_rule)  # type: yara.Rules
    console_results = []
    callback_result = {}
    rule.match(
        console_callback=lambda x: console_results.append(x),
        callback=lambda x: callback_result.update(x),
        data=data
    )
    callback_result["strings"] = [
        (offset, name, (data.encode() if type(data) is str else data).hex())
        for (offset, name, data) in callback_result["strings"]
    ]
    return {
        "file": {
            "bucket": bucket_name,
            "name": object_name
        },
        "console": console_results,
        "result": callback_result
    }


@celery_app.task(name="tasks.is_rule_valid")
def is_rule_valid(rule: str) -> bool:
    """
    Validate a yara rule

    :param rule: The rule to validate
    :return: Is the rule valid
    """
    try:
        yara.compile(source=rule)
        return True
    except yara.SyntaxError:
        return False

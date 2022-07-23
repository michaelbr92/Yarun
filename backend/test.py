import time
from pprint import pprint
from typing import List
from minio import Minio

from celery.result import AsyncResult
import urllib3

from tasks.rules import add, run_rule


rule_raw = """
import "console"
rule test{
    strings:
        $a = "aaa"
    condition:
        for all i in (1..#a): (console.log("a", @a[i])) and
        all of them
}
"""


data_raw = """
aadaadaa
bbbaaa
caaac
"""

client = Minio(
    "127.0.0.1:9000",
    access_key="admin",
    secret_key="Password1!",
    secure=False
)

# type: urllib3.response.HTTPResponse
# resp = client.get_object("files", "aaa.txt").data
# print(resp)

a = add.delay(1, 2)  # type: AsyncResult
tasks = [add.delay(1, 2)
         for _ in range(1)]  # type: List[AsyncResult]
uuids = [t.id for t in tasks]

for t in tasks:
    pprint(t.info)
    pprint(t.status)
    pprint(t.get())

    pprint(t.status)
    t.forget()

# for t in map(lambda uuid: AsyncResult(uuid), uuids):
#     print(t.info)
#     t.forget()
# time.sleep(4)
# for t in map(lambda uuid: AsyncResult(uuid), uuids):
#     t.forget()
#     print(t.info)

# time.sleep(4)

# for t in map(lambda uuid: AsyncResult(uuid), uuids):
#     print(t.info)
#     t.forget()
# # for t in tasks:

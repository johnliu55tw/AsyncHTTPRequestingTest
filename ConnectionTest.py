#!/usr/bin/env python3

import requests as reqs
import asyncio
import aiohttp
import time
import random


HOST = "http://localhost:5000"


def syncGetPatientsFromNurse(nurseName):
    session = reqs.Session()
    nurses = session.get(HOST + "/users", params={"name": nurseName}).json()
    if len(nurses) == 0:
        raise ValueError("Nurse {} cannot be found from the server".format(
            nurseName))

    firstMatchedId = nurses[0]["id"]

    patients = session.get(HOST + "/patients",
                           params={"nurseId": firstMatchedId}).json()
    if len(patients) == 0:
        raise ValueError("Nurse {} has no patients!".format(nurseName))

    return patients


async def asyncGetPatientsFromNurse(nurseName):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(HOST + "/users",
                                 params={"name": nurseName})
        nurses = await resp.json()
        if len(nurses) == 0:
            raise ValueError("Nurse {} cannot be found from the server".format(
                nurseName))

        firstMatchedId = nurses[0]["id"]

        resp = await session.get(HOST + "/patients",
                                 params={"nurseId": firstMatchedId})
        patients = await resp.json()
        if len(patients) == 0:
            raise ValueError("Nurse {} has no patients!".format(nurseName))

        return patients


def synchronous(names):
    result = list()
    for name in names:
        result.append(syncGetPatientsFromNurse(name))
    return result


def asynchronous(names):
    tasks = asyncio.gather(*[asyncGetPatientsFromNurse(name)
                             for name in names])
    return tasks


if __name__ == "__main__":
    print("Timing for synchronous method...")
    firstTime = time.time()
    syncResult = syncGetPatientsFromNurse("John")
    endTime = time.time()
    print("Synchronous method takes: {}s".format(endTime - firstTime))

    time.sleep(1)

    loop = asyncio.get_event_loop()
    print("Timing for asynchronous method...")
    firstTime = time.time()
    asyncResult = loop.run_until_complete(asyncGetPatientsFromNurse("John"))
    endTime = time.time()
    print("Asynchronous method takes: {}s".format(endTime - firstTime))

    assert syncResult == asyncResult

    print("Timing for synchronous method in multiple calls...")
    nurseNames = [random.choice(["John", "William"]) for _ in range(10)]
    firstTime = time.time()
    syncResult = synchronous(nurseNames)
    endTime = time.time()
    print("Synchronous method takes: {}s".format(endTime - firstTime))

    time.sleep(1)

    print("Timing for asynchronous method in multiple calls...")
    firstTime = time.time()
    asyncResult = loop.run_until_complete(asynchronous(nurseNames))
    endTime = time.time()
    print("Asynchronous method takes: {}s".format(endTime - firstTime))

    assert syncResult == asyncResult

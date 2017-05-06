#!/usr/bin/env python3

import requests as reqs
import asyncio
import aiohttp
import time
import random


HOST = "http://localhost:5000"


def getSalespersonNameList():
    users = reqs.get(HOST + "/users", params={"role": "sales"}).json()
    return [user["name"] for user in users]


def syncGetCustomersFromSales(salesName):
    with reqs.Session() as session:
        resp = session.get(HOST + "/users", params={"name": salesName})
        sales = resp.json()
        if len(sales) == 0:
            raise ValueError("Sales {} cannot be found from the server".format(
                salesName))

        firstMatchedId = sales[0]["id"]

        resp = session.get(HOST + "/customers",
                           params={"salesId": firstMatchedId})
        customers = resp.json()
        if len(customers) == 0:
            raise ValueError("Sales {} has no customers!".format(salesName))

        return customers


async def asyncGetCustomersFromSales(salesName):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(HOST + "/users", params={"name": salesName})
        sales = await resp.json()
        if len(sales) == 0:
            raise ValueError("Sales {} cannot be found from the server".format(
                salesName))

        firstMatchedId = sales[0]["id"]

        resp = await session.get(HOST + "/customers",
                                 params={"salesId": firstMatchedId})
        customers = await resp.json()
        if len(customers) == 0:
            raise ValueError("Sales {} has no customers!".format(salesName))

        return customers


def synchronous(names):
    result = list()
    for name in names:
        result.append(syncGetCustomersFromSales(name))
    return result


def asynchronous(names):
    tasks = asyncio.gather(*[asyncGetCustomersFromSales(name)
                             for name in names])
    return tasks


if __name__ == "__main__":
    # Timing for multiple requests
    salesNameList = getSalespersonNameList()
    randomSalesNames = [random.choice(salesNameList) for _ in range(10)]
    print("Timing for synchronous method in multiple calls...")
    firstTime = time.time()
    syncResult = synchronous(randomSalesNames)
    endTime = time.time()
    print("Synchronous method takes: {}s".format(endTime - firstTime))

    time.sleep(1)

    print("Timing for asynchronous method in multiple calls...")
    loop = asyncio.get_event_loop()
    firstTime = time.time()
    asyncResult = loop.run_until_complete(asynchronous(randomSalesNames))
    endTime = time.time()
    print("Asynchronous method takes: {}s".format(endTime - firstTime))

    assert syncResult == asyncResult

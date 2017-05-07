#!/usr/bin/env python3

import requests as reqs
import asyncio
import aiohttp
import time
import random


HOST = "http://localhost:5000"


def getRandomSalespersons(number):
    users = reqs.get(HOST + "/users", params={"role": "sales"}).json()
    return [random.choice([user["name"] for user in users])
            for _ in range(number)]


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
    return [syncGetCustomersFromSales(name) for name in names]


def asynchronous(names):
    loop = asyncio.get_event_loop()
    tasks = asyncio.gather(*[asyncGetCustomersFromSales(name)
                             for name in names])
    asyncResult = loop.run_until_complete(tasks)
    return asyncResult


if __name__ == "__main__":
    # Randomly generate 10 salespersons name from the server
    randomSalesNames = getRandomSalespersons(10)

    # Requesting synchonously
    print("Timing for synchronous method in multiple calls...")
    firstTime = time.time()
    syncResult = synchronous(randomSalesNames)
    endTime = time.time()
    print("Synchronous method takes: {0:.3f}s".format(endTime - firstTime))

    time.sleep(1)

    # Requesting asynchonously
    print("Timing for asynchronous method in multiple calls...")
    loop = asyncio.get_event_loop()
    firstTime = time.time()
    asyncResult = (asynchronous(randomSalesNames))
    endTime = time.time()
    print("Asynchronous method takes: {0:.3f}s".format(endTime - firstTime))

    # Make sure the results are identical
    assert syncResult == asyncResult

# Utilize the `asyncio` Module: Asynchronous HTTP Requests

## Introduction

The project wants to test how convenient the `asyncio` is for transforming a bunch of synchronous HTTP requests into aysnchronous, to make them faster!

## Dependencies

* `Python` >= 3.5 (for `async` and `await` syntax)
* `aiohttp`
* `Flask`
* `requests`
* `uWSGI`

See [`requirements.txt`](./requirements.txt) for more information.

## The HTTP Server

First we have to build a HTTP server from which the connection testing application could requests data. Here we are going to use [API Blueprint](https://apiblueprint.org/) for designing and documenting the API, [Flask](http://flask.pocoo.org/docs/0.12/) for building the server and [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) for running the server.

### For What?

The server stores information of a purchasing deparment in a company. It stores users information like names and roles (salesperson, manager, etc.) and some information about the customers of the company, like the salesperson who is responsible for the client.

### RESTful API

Please see [DockingAPIServer.apib](./DockingAPIServer.apib) for more information about how to interact with the server.

### Flask Server

Please see [DockingAPIServer.py](./DockingAPIServer.py) for more information. One thing worth noting is that, because we are doing request speed test, it is necessary to make the requests slow, acting like the server is doing something heavy, or we won't be able to see the difference. Thus, I added a `sleep` call in every routing function, and it is configurable by setting changing the line in code:

```
app.config["DELAY"] = 0.5  # Delay in seconds
```

### uWSGI: Starting the Server!

The reason why we need uWSGI (or other HTTP server) to run the Flask app is because the built-in HTTP server of Flask is single-threaded, which means while the Flask HTTP server is handling one request from one connection, it is impossible for it to handle another connection. This is not the case for most of the HTTP server, and becasuse we need to make several requests at the same time, this behavior will seriously affect the performance, regardless of making requests synchronously or asynchronously.

To start the `uWSGI` server, run the following command:

```
$ uwsgi --http 127.0.0.1:5000 --http-keepalive --so-keepalive --wsgi-file DockingAPIServer.py --callable app --processes 4 --threads 2
```

Or you could directly run the [`run_uwsgi.sh`](./run_uwsgi.sh).

```
$ bash run_uwsgi.sh
```

Which will start the server listening on `127.0.0.1:5000` with HTTP Keep-Alive enabled. Noted that if you change the name of the Flask application (`DockingAPIServer.py`), or the code, you have to specify the correct `--wsgi-file` and `--callable` option.

Noted that I installed uWSGI by `pip`. I've encounter some problem (`--wsgi-file` option not available) when I was trying to install uWSGI by `pacman`.

## The Connection Test

Let's say you want to fetch customers of the salesperson named "John", we first need to query the `/users` endpoint with query parameter `name=John`, then use the salesperson's `id` to query all his customers from the `/customers` endpoint with query parameter `salesId=id`. Therefore, 2 requests have to be made in order to fetch customers information for a salesperson.

### Synchronous HTTP Request

```
import requests as reqs

HOST = "http://localhost:5000"

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
```

The result of running the function with `"John"` as argument should be:

```
[
  {
    "id": "1",
    "name": "Andy Ziemmer",
    "salesId": "1"
  },
  {
    "id": "2",
    "name": "Michael Jordan",
    "salesId": "1"
  }
]
```

### Asynchronous HTTP Requests

Here we need the `aiohttp` package to do the async requests:

```
import aiohttp

HOST = "http://localhost:5000"

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
```

As you can see, except those `async` and `await` syntax (and a context manager for session), the structure of the code is not that different from its synchronous brother.

Because it is a **coroutine function**, we need an event loop to run it:

```
import asyncio

loop = asyncio.get_event_loop()
result = loop.run_until_complete(asyncGetCustomerFromSales("John"))
```

And the `result` will be the same:

```
[
  {
    "id": "1",
    "name": "Andy Ziemmer",
    "salesId": "1"
  },
  {
    "id": "2",
    "name": "Michael Jordan",
    "salesId": "1"
  }
]
```

### Testing the Requests

Imagine that we have a list of salespersons' name and we want to fetch the information of their customers. Here are functions for doing that in sync. and async. way.

```
# Given a list of names, return their customers synchronously
def synchronous(names):
    return [syncGetCustomersFromSales(name) for name in names]


# Given a list of names, return their customers asynchronously
def asynchronous(names):
    loop = asyncio.get_event_loop()
    # asyncio.gather is required for gathering results in sequence
    tasks = asyncio.gather(*[asyncGetCustomersFromSales(name)
                             for name in names])
    asyncResult = loop.run_until_complete(tasks)
    return asyncResult
```

Apparently there are more boilerplate codes for the async. version, but trust me, it's worth it.

Since I'm lazy so I want to genearte the list of names randomly from the server:

```
def getRandomSalespersons(number):
    users = reqs.get(HOST + "/users", params={"role": "sales"}).json()
    return [random.choice([user["name"] for user in users])
            for _ in range(number)]
```

Now, it's time to time it!

```
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
```

Here's the result:
```
Timing for synchronous method in multiple calls...
Synchronous method takes: 10.165s
Timing for asynchronous method in multiple calls...
Asynchronous method takes: 1.546s
```

The delay of the server is set to 0.5 second. Since fetching customers' information takes 2 requests to the server, so the synchronous version takes about 10 seconds to finished.

However, without many change of codes, the asynchronous version is almost 7 times faster! This is the power of asychronous code :D

## Conclusion


Asynchronization allows some optimization without abusing the multi-threading or multi-processing modules and dealing with all the synchronization between those threads/processes manually, as you can see from above. Since the introducing of `async` and `await` syntax in python 3.5, it's much easier to write and read the asynchronous code instead of using the weird generator and decorator pattern to implement asynchronization.

However, the API to the `asyncio` module is still incredibly complex. It has all sorts of terminologies and classes like `Future`, `Coroutine`, `Coroutine Function` and `Task`, and there are many ways to register a snippet of asynchronous code into the event loop. It took me a while comprehending all the information on the official websites and articles written by others in order to write this article.

Nevertheless, `asyncio` module did provide some handy APIs for quickly implementing some network codes, like [Transports and protocols](https://docs.python.org/3/library/asyncio-protocol.html#transports-and-protocols-callback-based-api). My other github project [AsyncIOServer](https://github.com/johnliu55tw/AsyncIOServer) shows how to create a simple TCP/SSL server with `asyncio` module.

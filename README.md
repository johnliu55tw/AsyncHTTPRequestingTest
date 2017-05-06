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
app.config['DELAY'] = 0.5  # Delay in seconds
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

Let's say we want to fetch customers of the salesperson named "John", we first need to query the `/users` endpoint with query parameter `name=John`, then use the salesperson's `id` to query all his customers from the `/customers` endpoint with query parameter `salesId=id`.

### Synchronous HTTP Request

```
import requests as reqs

HOST = 'http://localhost:5000

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

HOST = 'http://localhost:5000

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

### Timing

To Be Continue...

## Conclusion

To Be Continue...

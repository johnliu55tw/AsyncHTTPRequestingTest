# Utilize the `asyncio` Module: HTTP Requests

## Introduction

The project wants to test how convenient the `asyncio` is in transforming a bunch of synchronous HTTP requests into aysnchronous, to make them faster!

## Dependencies

* `Python` >= 3.5 (for `async` and `await` syntax)
* `aiohttp`
* `Flask`
* `requests`
* `uWSGI`

See [`requirements.txt`](./requirements.txt) for more information.

## First: The HTTP Server

First we have to build a HTTP server for which the connection testing application could requests data. Here we are going to use [API Blueprint](https://apiblueprint.org/) for designing and documenting the API, [Flask](http://flask.pocoo.org/docs/0.12/) for building the server and [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) for running the server.

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

Noted that I installed uWSGI by `pip`. I've encounter some problem (`--wsgi-file` option not available) by install uWSGI by `pacman`.

## The Connection Test

To Be Continue...

## Conclusion

To Be Continue...

#!/usr/bin/bash

uwsgi --http 127.0.0.1:5000 --http-keepalive --so-keepalive --wsgi-file DockingAPIServer.py --callable app --processes 4 --threads 2

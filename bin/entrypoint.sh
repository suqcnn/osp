#! /bin/bash

redis-server /etc/redis/redis.conf

daphne -b 0.0.0.0 -p 80 osp.asgi:application

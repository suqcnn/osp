#!/bin/bash

port=${port:-443}

redisServer=${redisServer}
redisDB=${redisDB:-0}
redisPassword=${redisPassword:-""}

if [[ ${redisServer} == "" ]]; then
    mkdir /var/lib/redis
    redis-server /etc/redis/redis.conf
fi

/ospserver \
    --port=${port} \
    --redis-server=${redisServer} \
    --redis-db=${redisDB} \
    --redis-password=${redisPassword}

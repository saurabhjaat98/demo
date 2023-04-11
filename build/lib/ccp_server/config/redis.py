###############################################################################
# Copyright (c) 2023-present CorEdge India Pvt. Ltd - All Rights Reserved     #
# Unauthorized copying of this file, via any medium is strictly prohibited    #
# Proprietary and confidential                                                #
# Written by Vicky Upadhyay <vicky@coredge.io>, Feb 2023                      #
###############################################################################
import json
from functools import wraps
from typing import Optional

from aioredis import create_redis_pool

from ccp_server.util import ccp_context
from ccp_server.util.constants import Constants

redis_pool = None


async def get_redis():
    global redis_pool
    if redis_pool is None:
        redis_pool = await create_redis_pool(Constants.REDIS_URL)
    return redis_pool


def cache(*, ttl: Optional[int] = Constants.REDIS_TTL_IN_SECONDS):
    def outer_wrapper(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis = await get_redis()
            user = ccp_context.get_logged_in_user() if ccp_context.get_logged_in_user() else ''
            hash_value = hash(user + func.__name__ + str(args) + str(kwargs))
            cache_key = hash_value
            cached_response = await redis.get(cache_key)
            if cached_response:
                return json.loads(cached_response)
            else:
                response = await func(*args, **kwargs)
                res_type = type(response)
                if isinstance(response, res_type):
                    await redis.set(cache_key, json.dumps(response), expire=ttl)
                else:
                    await redis.set(cache_key, response, expire=ttl)
                return response

        return wrapper

    return outer_wrapper

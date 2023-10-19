#!/usr/bin/env python3
"""Make a query to a url and return the html"""
import requests
import redis
from functools import wraps
from typing import Callable


def count(fn: Callable) -> Callable:
    """Count how many times a callable has been called and return callable"""
    @wraps(fn)
    def counter(*args, **kwargs):
        """count the calls to a callable and return it's value"""
        if len(args) != 1:
            return
        key: str = 'count:{}'.format(args[0])
        _redis = redis.Redis()
        _redis.incr(key)
        return fn(*args, **kwargs)
    return counter


@count
def get_page(url: str) -> str:
    """Get a page and return it's content"""
    _redis = redis.Redis()
    if _redis.get(url):
        page: str = _redis.get(url).decode('utf-8')
    else:
        page: str = requests.get(url).text
        _redis.setex(url, 10, page)
    return page

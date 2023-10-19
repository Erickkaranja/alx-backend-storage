#!/usr/bin/env python3
'''this module handle basic redis authentication.'''
import redis
from typing import Union, Callable
import uuid


class Cache:
    '''initializing class Cache'''

    def __init__(self, host="localhost", port=6379):
        '''initializing class cache constructor.'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''The method should generate a random key (e.g. using uuid).
           Args:
              data(Union[str, bytes, int, float]):
           Returns:
               unique uuid
        '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None):
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str):
        return self.get(key, fn=lambda data: data.decode('utf-8'))

    def get_int(self, key: str):
        return self.get(key, fn=lambda data: int(data))

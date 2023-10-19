#!/usr/bin/env python3
'''this module handle basic redis authentication.'''
import redis
import functools
from typing import Union, Callable, Any
import uuid


def call_history(method: Callable) -> Callable:
    @functools.wraps(method)
    def decorator(self, *args, **kwargs):
        """store input and output history of a method in redis"""
        input_name: str = method.__qualname__ + ":inputs"
        output_name: str = method.__qualname__ + ":outputs"
        self._redis.rpush(input_name, str(args))
        output: Any = method(self, *args, **kwargs)
        self._redis.rpush(output_name, output)
        return output
    return decorator


def count_calls(method: Callable):
    '''function that counts the numder of times a given function is called.'''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key: str = method.__qualname__
        self._redis.incr(key)

        result = method(self, *args, **kwargs)
        return result

    return wrapper


class Cache:
    '''initializing class Cache'''

    def __init__(self, host="localhost", port=6379):
        '''initializing class cache constructor.'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''The method should generate a random key (e.g. using uuid).
           Args:
              data(Union[str, bytes, int, float]): input data.
           Returns:
               unique uuid
        '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None):
        '''converts the value of the input key to a specified datatype.
           Args:
               keys(str):a key whose value is to be converted.
               callable(Callable): convertion type function to the key's
                        value.
           Returns:
               if callable is None, returns raw data of type 'b' else converted
               type of the data.
        '''
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str):
        '''converts the key's value to type str.
           Args:
               key(str): key's whose value is to be converted.
           Returns:
               type str of the converted value.
        '''
        return self.get(key, fn=lambda data: data.decode('utf-8'))

    def get_int(self, key: str):
        '''converts the key's value to type int.
           Args:
               key(str): key's whose value is to be converted.
           Returns:
               type int of the converted value.
       '''
        return self.get(key, fn=lambda data: int(data))


def replay(method: Callable) -> None:
    """Make a replay of history of method calls"""
    _redis = redis.Redis()
    count: int = int(_redis.get(method.__qualname__))
    inputkey: str = method.__qualname__ + ":inputs"
    outkey: str = method.__qualname__ + ":outputs"
    print("{} was called {} times:".format(method.__qualname__, count))
    ins: List = list(_redis.lrange(inputkey, 0, -1))
    outs: List = list(_redis.lrange(outkey, 0, -1))
    history: List = list(zip(ins, outs))
    for pair in history:
        print("{}(*{}) -> {}".format(method.__qualname__,
                                     pair[0].decode('utf-8'),
                                     pair[1].decode('utf-8')))

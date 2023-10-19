#!/usr/bin/env python3
'''this module handle basic redis authentication.'''
import redis
import functools
from typing import Union, Callable
import uuid
import pickle

r = redis.Redis(host='localhost', port=6379, db=0)

def call_history(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        # Get the qualified name of the decorated function
        function_name = f"{method.__qualname__}"
        print(function_name)

        # Create keys for input and output lists
        input_key = f"{function_name}:inputs"
        output_key = f"{function_name}:outputs"

        # Append input arguments to the input list
        input_data = str(args)
        r.rpush(input_key, input_data)

        # Execute the original function and store its output
        result = method(*args, **kwargs)
        output_data = pickle.dumps(result)  # Serialize the output to store in Redis
        r.rpush(output_key, output_data)

        return result

    return wrapper

def count_calls(method: Callable):
    '''function that counts the numder of times a given function is called.'''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__  # get qualified name of the method.
        # Increment the count for this method
        count = self._redis.incr(key)
        # Call the original method
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

#!/usr/bin/env python3
'''pymongo instance for inserting in a documents collection.'''


def insert_school(mongo_collection, **kwargs):
    '''function that inserts a new document in a collection based on kwargs.
       args:
           mongo_collection(mongodb collection): The collection of insertion.
           **kwargs(dictionary object): arguements to be passed to the
                    mongo_collection.
       Returns:
           newly inserted object's id.
    '''
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id

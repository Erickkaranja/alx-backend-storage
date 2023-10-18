#!/usr/bin/env python3
'''using pymongo to query mongodb'''


def list_all(mongo_collection):
    '''Use the find method to retrieve all documents in the collection
       args:
           mongo_collection(): collection from which we are listing it's
           documents.
       Returns:
           a list of all documents in the collection else empty list.
    '''
    cursor = mongo_collection.find({})
    documents = []

    for document in cursor:
        documents.append(document)

    return documents

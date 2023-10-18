#!/usr/bin/env python3
'''using pymongo to create mongo db instances.'''


def schools_by_topic(mongo_collection, topic):
    '''Python function that returns the list of school having a specific topic
       args:
           mongo_collection(mongodb collection): the collection of check.
           topic(string): topic of search.
       Returns:
           a school with a given topic.
    '''

    fetch = mongo_collection.find({'topics': {'$in': [topic]}})
    return [item for item in fetch]

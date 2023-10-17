#!/usr/bin/env python3
'''creating a mongodb instance using pymongo'''
def update_topics(mongo_collection, name, topics):
    '''changes all topics of a school document based on the name.
       args:
           mongo_collection(mongodb collection): collection whose
                            document is to be updated.
           name(collection object): attribute name to be updated.
           topics(collection object): object attribute of updating.
       Returns:
           updates the queried object.
    '''

    school_query = {"name": name}
    school = mongo_collection.find_one(school_query)
    if school:
        mongo_collection.update_one(school_query, {"$set": {"topics": topics}})

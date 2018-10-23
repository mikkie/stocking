# -*-coding=utf-8-*-
__author__ = 'aqua'

import pymongo
import json

client = pymongo.MongoClient('mongodb://pig:pigpiggo@localhost:27017/stocking')
for doc in client['stocking']['config'].find({'t1' : {'$exists' : True}}):
    print(doc['t1']['ydls'])
    print(doc['t1']['trade']['enable'])
    print(doc['t1']['ydls']['stop_p'])
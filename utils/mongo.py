# -*- coding: utf-8 -*-
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.dytt
collection = db.dytt

class MongoConnect(object):
    """
    mongodb 操作.
    """

    def __init__(self, address, port):
        client = MongoClient(address, port)
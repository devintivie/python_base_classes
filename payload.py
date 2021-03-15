import json

class payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

class object_view(object):
    def __init__(self, d):
        self.__dict__ = d
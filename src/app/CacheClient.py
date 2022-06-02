
from abc import abstractmethod


class CacheClient:
    @abstractmethod
    def get(self, key):
        pass


    @abstractmethod
    def remove(self, key):
        pass

    
    @abstractmethod
    def insert(self, key, data={}):
        pass

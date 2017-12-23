# coding: utf-8
import redis
from collector import settings


class SimpleHash:
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(value.__len__()):
            ret += self.seed*ret+ord(value[i])
        return (self.cap-1) & ret


class BloomFilter:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(BloomFilter, cls).__new__(cls)
            return cls._instance
        return cls._instance

    def __init__(self):
        self.bit_size = 1 << 25
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.r = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)
        self.hashFunc = []
        for i in range(self.seeds.__len__()):
            self.hashFunc.append(SimpleHash(self.bit_size, self.seeds[i]))

    def isContains(self, str_input, name):
        if not str_input:
            return False
        if str_input.__len__() == 0:
            return False
        ret = True
        for f in self.hashFunc:
            loc = f.hash(str_input)
            ret = ret & self.r.getbit(name, loc)
        return ret

    def insert(self, str_input, name):
        for f in self.hashFunc:
            loc = f.hash(str_input)
            self.r.setbit(name, loc, 1)

BloomInstance = BloomFilter()
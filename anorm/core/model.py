"""
Basic Model realization
"""
import asyncio
import asyncpg


class ModelMeta:
    def __new__(cls, clsname, bases, dct):
        pass


class BaseModel:
    __metaclass__ = ModelMeta

    def __init__(self):
        pass

import os
from src.interface import DBDB

__all__ = ['DBDB', 'connect']


def connect(dbname):
    try:
        with open(dbname, 'r+b') as f:  
            return DBDB(f)
    except IOError:
        with open(dbname, os.O_RDWR | os.O_CREAT) as fd:
            f = os.fdopen(fd, 'r+b')
            return DBDB(f)

import os
import sys
import enum

class SearchFilter(enum.Enum): 
    name = 1
    phone = 2
    address = 3

def openDataStorage(dataStorageName):
    try:
        f = open("{}".format(dataStorageName),"w")
        return f
    except IOError as e:
        raise IOError("Error Opening File: [{}]".format(e))
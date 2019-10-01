import json
from collections import namedtuple

class Entry(object):
    """
    Base Entry class, each entry in a phone book will be 
    based on this entry object
    """
    def __init__(self, name, address, phoneNumber):
        self.name = name
        self.address = address
        self.phoneNumber = phoneNumber
    
    def display(self):
        return "Name: {}\nAddress: {}\nPhone: {}".format(self.name, self.address, self.phoneNumber)
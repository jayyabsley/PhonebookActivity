import os
import re
import sys
import warnings
from pb_util import openDataStorage, SearchFilter
from typing import List
from entry import Entry

# Entries container for all phone book entries for serialisation
class PhonebookContainer(object):
    def __init__(self, entries: List[Entry]):
        self.entries = entries

    def add(self, new_entry, force):
        '''
        Add data to container, entry must be of type (Entry)
        '''
        if not force:
            for data in self.entries:
                if new_entry.phoneNumber == data.phoneNumber:
                    print ("invalid: duplicate entry found")
                    return
        
        self.entries.append(new_entry)

    def get_attribute_list(self):
        """
        Get all attribute keys stores in Entries
        """
        attributes = [attr for attr in vars(self.entries[0]) if not attr.startswith('__')]
        return attributes

    def to_dict(self):
        """
        Convert class data table to hash table
        dict will contain all data in entries as will not need
        to be manually added here
        """
        d = {}
        i = 0
        for entry in self.entries:
            d[i] = {}
            attributes = self.get_attribute_list()
            print (attributes)
            for data in attributes:
                d[i][data] = entry.__getattribute__(data)
            i = i + 1
        return d

    def find(self,search_type:SearchFilter, search_params, use_regx):
        '''
        Search for a specific dataset
        '''
        regx = re.compile(search_params)
        found_results = []
        if search_type is SearchFilter.name:
            for i in self.entries:
                if use_regx and regx.match(i.name):
                    found_results.append(i)
                elif search_params in i.name:
                    found_results.append(i)
        if search_type is SearchFilter.phone:
            if search_type is SearchFilter.phone:
                for i in self.entries:
                    if use_regx and regx.match(i.phone):
                        found_results.append(i)
                    elif search_params in i.phone:
                        found_results.append(i)
        if search_type is SearchFilter.address:
            if search_type is SearchFilter.address:
                for i in self.entries:
                    if use_regx and regx.match(i.address):
                        found_results.append(i)
                    elif search_params in i.address:
                        found_results.append(i)
        return found_results

    def display(self):
        for i in self.entries:
            print ("--------")
            print (i.display())
            print ("---------")
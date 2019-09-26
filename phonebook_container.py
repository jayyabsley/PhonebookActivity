import os
import re
import sys
import warnings
from pb_util import *
from typing import List
from entry import Entry

# Entries container for all phone book entries for serialisation
class PhonebookContainer(object):
    def __init__(self, entries: List[Entry]):
        self.entries = entries

    def add(self, new_entry, force):
        # Check for unique data against phoneNumber
        if not force:
            for data in self.entries:
                if new_entry.phoneNumber == data.phoneNumber:
                    print ("invalid: duplicate entry found")
                    return
        
        self.entries.append(new_entry)

    def find(self,search_type:SearchFilter, search_params, use_regx):
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
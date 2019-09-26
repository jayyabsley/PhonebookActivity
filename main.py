import os
import sys
import argparse
import glob
import enum
import json

from pb_util import *
from typing import List
from entry import Entry
from phonebook_container import PhonebookContainer

class SupportedFormats(enum.Enum): 
    JSON = 1
    XML = 2

def create_phonebook(phonebook_name):
    filename = '%s' % phonebook_name
    if os.path.exists(filename):
        raise IOError("File [{0}] already exist".format(phonebook_name))
        quit()
    with open(filename, 'w') as f:
        pass


def load_phonebook(phonebook_name):
    with open(phonebook_name, 'r') as f:
        try:
            distros_dict = json.load(f)
            loaded_json = json.loads(distros_dict)
            for entry in loaded_json['entries']:
                new_entry = create_entity(
                    entry['name'],
                    entry['address'],
                    entry['phoneNumber'])
                try:
                    phonebook_data.add(new_entry, True)
                except UnboundLocalError:
                    phonebook_data = PhonebookContainer([new_entry])
            
            return phonebook_data
        except json.decoder.JSONDecodeError:
             pass
        

# display content of phonebook through CLI
def display_phonebook_content(phonebook_name):
    print(load_phonebook(phonebook_name).display())

# create new entity from unformed data
def create_entity(name, address, number):
    new_user = Entry(name, address, number)
    return new_user


# add a new name
def add_entry(new_entity, phonebook_name, force):
    try:
        phonebook_data = load_phonebook(phonebook_name)
        phonebook_data.add(new_entity, force)
    except AttributeError:
        phonebook_data = PhonebookContainer([new_entity])

    with openDataStorage(phonebook_name) as output_file:
        try:
            json_data = json.dumps(
            phonebook_data.__dict__,
            default=lambda o: o.__dict__)
            json.dump(json_data, output_file)
        except TypeError as e:
            print("Unable to serialize the object: {}".format(e))
        


def update_entry(entity_found, new_entity):
    pass


def lookup_entry(phonebook_name, search_type:SearchFilter, search_params, use_regx):
    phonebook_data = load_phonebook(phonebook_name)
    elements_found = phonebook_data.find(search_type, search_params, use_regx)
    if len(elements_found) > 0:
        print ('{} RESULTS FOUND'.format(len(elements_found)))
        if use_regx:
            print ('> results searched using regular expression\n')
        for element in elements_found:
            print (element.display(), '\n')
    else:
        print ('no results found.')


def delete_entry(entry):
    pass


parser = argparse.ArgumentParser()


subparsers = parser.add_subparsers(help='commands', dest='commandName')

p = subparsers.add_parser(
    'create',
    help='(create) will create an exported dataset')
p.add_argument('phonebook_name', action='store', help='name of datastore')

p = subparsers.add_parser('lookup', help='search for existing entry')
p.set_defaults(nameFilter=False, phoneFilter=False, addressFilter=False, use_regx=False, filter='')
p.add_argument('phonebook_name', action='store', help='name of datastore')
group = p.add_mutually_exclusive_group(required=True)
group.add_argument('--name', dest='nameFilter', action='store_true')
group.add_argument('--phone', dest='phoneFilter', action='store_true')
group.add_argument('--address', dest='addressFilter', action='store_true')
p.add_argument('--search', dest='filter', action='store', required=True)
p.add_argument('--regx', dest='use_regx', action='store_true', required=False)

p = subparsers.add_parser('load', help='load all entries')
p.add_argument('phonebook_name', action='store', help='name of datastore')

p = subparsers.add_parser(
    'add', help='(add) will append a new entry into the stored container')
p.set_defaults(force=False)
p.add_argument('name', action='store', help='name of person entry')
p.add_argument('address', action='store', help='person Address')
p.add_argument('number', action='store', help='contact number')
p.add_argument('phonebook_name', action='store', help='data file name')
p.add_argument(
    '--force',
    dest='force',
    action='store_true',
    help='force duplicates')

p = subparsers.add_parser(
    'export',
    help='(export) the stored data as a desired output format')
p.add_argument(
    'filename',
    action='store',
    help='export filename')
p.add_argument(
    '--xml',
    dest='exportXML',
    action='store_true',
    help='output format will be XML')
p.add_argument(
    '--json',
    dest='exportJSON',
    action='store_true',
    help='output format will be JSON')


def main():
    args = parser.parse_args()
    if args.commandName == 'create':
        create_phonebook(args.phonebook_name)
    elif args.commandName == 'add':
        new_entity = create_entity(args.name, args.address, args.number)
        add_entry(new_entity, args.phonebook_name, args.force)
    elif args.commandName == 'lookup':
        if args.phoneFilter:
            searchCat = SearchFilter.phone
        if args.nameFilter:
            searchCat = SearchFilter.name
        if args.addressFilter:
            searchCat = SearchFilter.address
        lookup_entry(args.phonebook_name, searchCat, args.filter, args.use_regx)
    elif args.commandName == 'load':
        display_phonebook_content(args.phonebook_name)
    elif args.commandName == 'lookup':
        display_phonebook_content(args.phonebook_name)
    # elif args.commandName == 'update':
    #     lookup_params = args.pop(0)
    #     lookup_entry(args)
    #     if lookup_params:
    #         May need to delete original entry then add new entry
    #         update_entry(lookup_entry)


if __name__ == '__main__':
    main()

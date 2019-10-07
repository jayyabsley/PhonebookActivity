import os
import sys
import argparse
import glob
import enum
import json
import csv

from typing import List
import filestreamers
from pb_util import openDataStorage, SearchFilter
from phonebook_container import PhonebookContainer
from entry import Entry

class SupportedFormats(enum.Enum): 
    JSON = 1 # Default Datastore
    CSV = 2
    HTML = 3

def create_phonebook(phonebook_name):
    '''
    Create an empty phonebook datastore
    '''
    filename = '%s' % phonebook_name
    if os.path.exists(filename):
        # Raise error if file exists and inform the user
        raise IOError("File [{0}] already exist".format(phonebook_name))
    with open(filename, 'w') as f:
        pass

def load_phonebook(phonebook_name):
    '''
    Load data in from an existing datastore
    '''
    with open(phonebook_name, 'r') as f:
        try:
            # Attempt to load data from existing phonebook dataset
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
                    # Unable to find existing dataset create new Phonebook Container
                    phonebook_data = PhonebookContainer([new_entry])
            
            return phonebook_data
        except json.decoder.JSONDecodeError as e:
            # JSON Error
            print ("JSON Error: {}".format(e))


def export_phonebook(phonebook_name, export_type:SupportedFormats, output_filename="export"):
    '''
    Export data from a specified datastore to an specified dataformat
    To add a new data format you will need to add a new streamer within FILESTREAMERS module
    It must inherit from FileStreamerBaseClass
    '''
    loaded_data = load_phonebook(phonebook_name)

    if export_type == SupportedFormats.JSON:
        csv_exporter_instance = filestreamers.define('jsonfilestreamer', name='JSONExport')
        csv_exporter_instance.export_phonebook_data(loaded_data.to_dict(), output_filename)
    
    if export_type == SupportedFormats.CSV:
        csv_exporter_instance = filestreamers.define('csvfilestreamer', name='CSVExport')
        csv_exporter_instance.export_phonebook_data(loaded_data.to_dict(), output_filename)

    if export_type == SupportedFormats.HTML:
        html_exporter_instance = filestreamers.define('htmlfilestreamer', name='HTMLExport')
        html_exporter_instance.export_phonebook_data(loaded_data.to_dict(), output_filename)

# create new entity from unformed data
def create_entity(name, address, number):
    '''
    Form entry object from a dataset
    '''
    new_user = Entry(name, address, number)
    return new_user


# add a new name
def add_entry(new_entity, phonebook_name, force):
    '''
    Add new entry to phonebook
    '''
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


def lookup_entry(phonebook_name, search_type:SearchFilter, search_params, use_regx, export_results_dest):
    '''
    Lookup entry using simple contains search
    Expanded to use regx for more refined search
    '''
    phonebook_data = load_phonebook(phonebook_name)
    try:
        elements_found = phonebook_data.find(search_type, search_params, use_regx)
        if len(elements_found) > 0:
            print ('{} RESULTS FOUND'.format(len(elements_found)))
            if use_regx:
                print ('> results searched using regular expression\n')
            for element in elements_found:
                for el in elements_found:
                    try:
                        result_pb.add(el, True)
                    except UnboundLocalError:
                        # Unable to find existing dataset create new Phonebook Container
                        result_pb = PhonebookContainer([el])
                print (element.display(), '\n')
                if len(export_results_dest) > 0:
                    print (result_pb.to_dict())
                    print ("Outputting to {}".format(export_results_dest))
                    json_exporter_instance = filestreamers.define('jsonfilestreamer', name='JSONExport')
                    json_exporter_instance.export_phonebook_data(result_pb.to_dict(), export_results_dest)
                
        else:
            print ('no results found.')
    except AttributeError:
        print ("No entries found in dataset")

### Args Parser
parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(help='commands', dest='commandName')

# Create Datastore Args
p = subparsers.add_parser('create', help='(create) will create an exported dataset')
p.add_argument('phonebook_name', action='store', help='name of datastore')

# Lookup\Search Args
p = subparsers.add_parser('lookup', help='search for existing entry')
p.set_defaults(nameFilter=False, phoneFilter=False, addressFilter=False, use_regx=False, filter='')
p.add_argument('phonebook_name', action='store', help='name of datastore')
group = p.add_mutually_exclusive_group(required=True)
group.add_argument('--name', dest='nameFilter', action='store_true')
group.add_argument('--phone', dest='phoneFilter', action='store_true')
group.add_argument('--address', dest='addressFilter', action='store_true')
p.add_argument('--search', dest='filter', action='store', required=True)
p.add_argument('--regx', dest='use_regx', action='store_true', required=False)
p.add_argument('--export', dest='export_dest', action='store', required=False)

# Add Args
p = subparsers.add_parser('add', help='(add) will append a new entry into the stored container')
p.set_defaults(force=False)
p.add_argument('name', action='store', help='name of person entry')
p.add_argument('address', action='store', help='person Address')
p.add_argument('number', action='store', help='contact number')
p.add_argument('phonebook_name', action='store', help='data file name')
p.add_argument('--force', dest='force', action='store_true', help='force duplicates')

# Export Args
p = subparsers.add_parser('export', help='(export) the stored data as a desired output format')
p.add_argument('phonebook_name', action='store', help='dataset filename')
p.add_argument('--json', dest='exportJSON', action='store_true', help='output format will be JSON')
p.add_argument('--csv', dest='exportCSV', action='store_true', help='output format will be CSV')
p.add_argument('--html', dest='exportHTML', action='store_true', help='output format will be HTML')

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
        lookup_entry(args.phonebook_name, searchCat, args.filter, args.use_regx, args.export_dest)
    elif args.commandName == 'export':
        if args.exportJSON:
            export_phonebook(args.phonebook_name, SupportedFormats.JSON)
        if args.exportCSV:
            export_phonebook(args.phonebook_name, SupportedFormats.CSV)
        if args.exportHTML:
            export_phonebook(args.phonebook_name, SupportedFormats.HTML)
            

if __name__ == '__main__':
    main()
    

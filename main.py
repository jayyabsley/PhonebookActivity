import os
import sys
import argparse
import glob
import enum
import json
import csv

from pb_util import *
from typing import List
from entry import Entry
from phonebook_container import PhonebookContainer

class SupportedFormats(enum.Enum): 
    JSON = 1 # Default Datastore
    CSV = 2

def create_phonebook(phonebook_name):
    filename = '%s' % phonebook_name
    if os.path.exists(filename):
        # Raise error if file exists and inform the user
        raise IOError("File [{0}] already exist".format(phonebook_name))
    with open(filename, 'w') as f:
        pass

def load_phonebook(phonebook_name):
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
        

# display content of phonebook through CLI
def display_phonebook_content(phonebook_name, export_to_html):
    loaded_data = load_phonebook(phonebook_name)
    if export_to_html:
        output_to_html(loaded_data, phonebook_name)
    else:
        print(loaded_data.display())

# outputing content to a html file with basic templated content
def output_to_html(phonebook_entries, phonebook_name):
    with open('output.html', 'w') as htmlFile:
        htmlFile.write('<html>')
        htmlFile.write('<body>')
        htmlFile.write('<table>')
        htmlFile.write('<h1>Output from {}</h1>'.format(phonebook_name))
        for entry in phonebook_entries.entries:
            htmlFile.write('Name: {}<br>'.format(entry.name))
            htmlFile.write('Phone Number: {}<br>'.format(entry.phoneNumber))
            htmlFile.write('Address: {}<br>'.format(entry.address))
            htmlFile.write('<br>')
        htmlFile.write('</tr>')
        htmlFile.write('</table>')
        htmlFile.write('</body>')
        htmlFile.write('</html>')
        htmlFile.close()

def export_phonebook(phonebook_name, export_type:SupportedFormats):
    loaded_data = load_phonebook(phonebook_name)
    if export_type == SupportedFormats.CSV:
        print ('Exporting CSV')
        output_to_csv(loaded_data)

# Basic implementation of a CSV output.
# TODO: Move this into pb_util but need to restructure to avoid circular dependency
def output_to_csv(phonebook_entires):
    with open('phonebook_output.csv', mode='w') as csv_file:
        phonebook_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        phonebook_writer.writerow(['name', 'phone', 'address'])
        for entry in phonebook_entires.entries:
            phonebook_writer.writerow([entry.name, entry.phoneNumber, entry.address])


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

# Lookup entry using simple contains search
# Expanded to use regx for more refined search
def lookup_entry(phonebook_name, search_type:SearchFilter, search_params, use_regx):
    phonebook_data = load_phonebook(phonebook_name)
    try:
        elements_found = phonebook_data.find(search_type, search_params, use_regx)
        if len(elements_found) > 0:
            print ('{} RESULTS FOUND'.format(len(elements_found)))
            if use_regx:
                print ('> results searched using regular expression\n')
            for element in elements_found:
                print (element.display(), '\n')
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

# Load Args
p = subparsers.add_parser('load', help='load all entries')
p.add_argument('phonebook_name', action='store', help='name of datastore')
p.add_argument('--html', dest='export_html', action='store_true', required=False)

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
p.add_argument('--csv', dest='exportCSV', action='store_true', help='output format will be CSV')

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
        display_phonebook_content(args.phonebook_name, args.export_html)
    elif args.commandName == 'export':
        if args.exportCSV:
            export_phonebook(args.phonebook_name, SupportedFormats.CSV)
            

if __name__ == '__main__':
    main()

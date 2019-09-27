# Phonebook Technical Task
Technical Task Assessment. 

In Python or C++ write a module or small library which shows how you would take a set of personal data, where each record contains:

name
address
phone number
And:

build a simple API allowing you to add new records, filter users (e.g "name=Joe*") based on some simple search syntax like Glob.
support serialisation in 2 or more formats (e.g JSON, Yaml, XML, CSV etc)
Display the data in 2 or more different output formats (no need to use a GUI Framework, use e.g text output/HTML or any other human readable format).
Add a command line interface to add records, and display/convert/filter the whole data set
Write it in such a way that it would be easy for a developer to extend the system e.g

to add support for additional storage formats
to query a list of currently supported formats
This should ideally show Object-Oriented Design and Design Patterns Knowledge, we’re not looking for use of advanced Language constructs.

Please provide reasonable Unit Test coverage and basic API documentation

## Getting Started

This project was developed using Python 3.7.4:e09359112e using default modules.

### Prerequisites

No additional PIP requirements are necessary.

### Installing

Small module that can be imported from main.py

For a rundown for commands

```
>> python main.py add -h

-------------
expected output
-------------
usage: main.py [-h] {create,lookup,load,add,export} ...

positional arguments:
  {create,lookup,load,add,export}
                        commands
    create              (create) will create an exported dataset based on the
                        stored binary file
    lookup              search for existing entry
    load                load all entries
    add                 (add) will append a new entry into the stored
                        container
    export              (export) the stored data as a desired output format

optional arguments:
  -h, --help            show this help message and exit
```
```
>> python main.py add -h

-------------
expected output

usage: main.py add [-h] name address number phonebook_name

positional arguments:
  name            name of person entry
  address         person Address
  number          contact number
  phonebook_name  data file name

optional arguments:
  -h, --help      show this help message and exit
```

Additional help information has been added where additional params are required

```
python main.py -h
```

## Running the tests

Tests have been developed using the inbuilt unittest module included with Python

To execute the unittests

```
python test.py -v

------------
expected output

test_add_new_entry (__main__.TestPhonebook) ... ok
test_create_entity (__main__.TestPhonebook) ... ok
test_phonebook_create (__main__.TestPhonebook) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.003s

OK
```

Checked using pycodestyle (optional external checker)

```
pycodestyle --first main.py
```

## Using the module

On first run you will need to create a json storage for the dataset to save its persistent data.

### Phonebook Creation

The phonebook will always be required to be defined to allow compatibility with external API's

*Example (powershell)*
```
python .\main.py create export.json
```
This will create an empty container

### Phonebook Creation
*Example (powershell)*
```
python .\main.py create export.json
```

### Add to Phonebook
*Example (powershell)*
```
python .\main.py add "First Last" "123 Fake St" "0404 040 040" export.json
python .\main.py add "Test User" "35/23 Test Ave" "02 9595 8484" export.json
```

### Display Content from Datafile
*Example (powershell)*
```
python .\main.py load export.json
```

Export Dataset as HTML file (output.html)
```
python .\main.py load export.json --html
```

### Search for content in Dataset

positional arguments:
  phonebook_name   name of datastore

single required arguments:
  --name
  --phone
  --address

required search filter argument
  --search "FILTER"

optional argument
  --regx (optional)

*Example (powershell)*
```
python .\main.py lookup export.json --name --search First
```
> Sample Output
```
1 RESULTS FOUND
Name: First Last
Address: 123 Fake St
Phone: 0404 040 040
```

### Add to Phonebook

Exporting dataset to CSV

```
python .\main.py export export.json --csv
```
This will create a file 'phonebook_output.csv'
Simple implmentation for now, wanting to expand on this more depending on time.
Also want to move a lot of this export function to utils but unable to class creation and cirular dependecies.


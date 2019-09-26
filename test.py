import main
import entry
import os
import json
import unittest

class TestPhonebook(unittest.TestCase):
    filename = "unittest.json"

    # Remove the file after the test
    def tear_down(self):  
        os.remove(self.filename)

    # Test creation of blank JSON storage container
    def test_phonebook_create(self):
        main.create_phonebook(self.filename)
        self.assertTrue(os.path.exists(self.filename))
        self.tear_down()
        
    # Test creation of a fresh entity on its own
    def test_create_entity(self):
        testName = "Create Test"
        testAddress = "123 Test Ave"
        testPhone = "0404 049 834"
        newEntry = main.create_entity(testName, testAddress, testPhone)

        self.assertEqual(newEntry.name, testName)
        self.assertEqual(newEntry.address, testAddress)
        self.assertEqual(newEntry.phoneNumber, testPhone)

    # Will create a new entry, add it to a new book and then validate that output JSON
    def test_add_new_entry(self):
        main.create_phonebook(self.filename)
        testName = "Add Test"
        testAddress = "321 Test Ave"
        testPhone = "0404 040 404"
        newEntry = main.create_entity(testName, testAddress, testPhone)

        main.add_entry(newEntry, self.filename, False)
        with open(self.filename, 'r') as f:
             self.assertTrue(json.load(f))
        self.tear_down()
        
    

if __name__ == '__main__':
    unittest.main()
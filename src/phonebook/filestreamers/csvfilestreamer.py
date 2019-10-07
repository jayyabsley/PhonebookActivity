from . import FileStreamerBaseClass
import csv

class Csvfilestreamer(FileStreamerBaseClass):

    def __init__(self, name=None):
        FileStreamerBaseClass.__init__(self, name)

    def export_phonebook_data(self, data_dict:dict, file_output_location):
        """
        Export data as CSV, this will take in a dict and extract all datakeys and create a CSV
        file based on the data given, regardless of dict size.
        """
        with open("{}.csv".format(file_output_location), mode='w') as csv_file:
            output_csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            keys = data_dict[0].keys()
            output_csv_writer.writerow(keys)
            for entry in data_dict.values():
                output_csv_writer.writerow(entry.values())
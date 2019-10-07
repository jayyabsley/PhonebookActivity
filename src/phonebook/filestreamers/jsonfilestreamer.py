from . import FileStreamerBaseClass
import json

class Jsonfilestreamer(FileStreamerBaseClass):

    def __init__(self, name=None):
        FileStreamerBaseClass.__init__(self, name)

    def export_phonebook_data(self, data_dict:dict, file_output_location):
        """
        Export data as JSON, this will take in a dict and extract all datakeys and create a JSON
        file based on the data given, regardless of dict size.
        """
        print (data_dict)
        with open("{}.json".format(file_output_location), mode='a+') as output_file:
                try:
                    json.dump(data_dict, output_file)
                except TypeError as e:
                    print("Unable to serialize the object: {}".format(e))


            # output_csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # keys = data_dict[0].keys()
            # output_csv_writer.writerow(keys)
            # for entry in data_dict.values():
            #     output_csv_writer.writerow(entry.values())
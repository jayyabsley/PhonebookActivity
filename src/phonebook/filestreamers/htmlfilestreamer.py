from . import FileStreamerBaseClass

class Htmlfilestreamer(FileStreamerBaseClass):

    def __init__(self, name=None):
        FileStreamerBaseClass.__init__(self, name)

    def export_phonebook_data(self, data_dict:dict, file_output_location):
        """
        Export data as HTML with massaged presentation, this will however still include all data regardless 
        of data being added or removed.
        this will take in a dict and extract all datakeys and create a CSV
        file based on the data given, regardless of dict size.
        """
        with open("{}.html".format(file_output_location), mode='w') as html_file:
            keys = data_dict[0].keys()
            html_file.write('<html>')
            html_file.write('<body>')
            html_file.write('<table>')
            for entry in data_dict.values():
                print ("entry: {}".format(entry))
                for data_name in keys:
                    print (entry.get("name"))
                    html_file.write('{}: {}<br>'.format(data_name, entry.get("{}".format(data_name))))
                    html_file.write('<br>')
            html_file.write('</tr>')
            html_file.write('</table>')
            html_file.write('</body>')
            html_file.write('</html>')
            html_file.close()
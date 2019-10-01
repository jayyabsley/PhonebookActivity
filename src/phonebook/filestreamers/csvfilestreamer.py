from . import FileStreamerBaseClass

class Csvfilestreamer(FileStreamerBaseClass):

    def __init__(self, name=None):
        FileStreamerBaseClass.__init__(self, name)

    def export_phonebook_data(self):
        print ("Do Stuff")
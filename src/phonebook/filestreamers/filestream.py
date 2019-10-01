# import phonebook.entry
# import phonebook.phonebook_container
from abc import ABCMeta, abstractmethod

class FileStreamerBaseClass(metaclass=ABCMeta):
    def __init__(self, name=None):
        pass
    
    @abstractmethod
    def export_phonebook_data(self):
        pass
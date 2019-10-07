
from importlib import import_module

from .filestream import FileStreamerBaseClass

def define(exporter_name, *args, **kwargs):
    '''
    get an instance of a module within filestreamers.
    instance must inherit from FileStreamerBaseClass
    Methods:
        export_phonebook_data (@abstacemethod)
    '''
    try:
        if '.' in exporter_name:
            mod, classname = exporter_name.rsplit('.', 1)
        else:
            mod = exporter_name
            classname = exporter_name.capitalize()

        filestreamer_module = import_module('.' + mod, package='filestreamers')

        exporter_class = getattr(filestreamer_module, classname)

        instance = exporter_class(*args, **kwargs)

    except (AttributeError, ModuleNotFoundError):
        raise ImportError('{} is not part of our exporter collection!'.format(exporter_name))
    else:
        print ("{} {}".format(exporter_class, exporter_name))
        if not issubclass(exporter_class, FileStreamerBaseClass):
            raise ImportError("Unable to import {}!".format(exporter_name))

    return instance
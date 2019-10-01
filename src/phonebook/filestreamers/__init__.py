
from importlib import import_module

from .filestream import FileStreamerBaseClass

def define(exporter_name, *args, **kwargs):
    try:
        if '.' in exporter_name:
            module_name, class_name = exporter_name.rsplit('.', 1)
        else:
            module_name = exporter_name
            class_name = exporter_name.capitalize()

        animal_module = import_module('.' + module_name, package='filestreamers')

        exporter_class = getattr(animal_module, class_name)

        instance = exporter_class(*args, **kwargs)

    except (AttributeError, ModuleNotFoundError):
        raise ImportError('{} is not part of our exporter collection!'.format(exporter_name))
    else:
        if not issubclass(exporter_class, exporter_name):
            raise ImportError("We currently don't have {}, but you are welcome to send in the request for it!".format(animal_class))

    return instance
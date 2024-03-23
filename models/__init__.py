#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""

import os
from .state import State
from .city import City
from .user import User
from .place import Place
from .amenity import Amenity
from .review import Review

storage_env = os.environ.get('HBNB_TYPE_STORAGE')
if storage_env == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()

__all__ = [
    'State', 'City', 'User', 'Place', 'Amenity',
    'Review', 'storage', 'storage_env']

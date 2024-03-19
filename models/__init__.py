#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""

import os
storage_env = os.environ.get('HBNB_TYPE_STORAGE')
if storage_env == 'db':
	from models.engine.db_storage import dbStorage
	storage = dbStorage()
	storage.relaod()
else:
	from models.engine.file_storage import FileStorage
	storage = FileStorage()
	storage.reload()

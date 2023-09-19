#!/usr/bin/python3

from os import getenv
storage = None
"""
This code block is checking the value of
the environment variable "HBNB_TYPE_STORAGE".
"""

if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()

#!/usr/bin/python3
"""
This module defines a base class for all models in our hbnb clone
The class defines a base class for all models in a hbnb clone,
providing common attributes and methods.
"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from models import storage
from os import getenv
Base = declarative_base()


class BaseModel:
    """
    A base class for all hbnb models
    The above class is a base class for all hbnb models,
    providing common attributes and methods such as
    id, created_at, updated_at, save, to_dict, and delete.
    """
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if 'id' not in kwargs:
                kwargs['id'] = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                kwargs['created_at'] = datetime.now()
            else:
                kwargs['created_at'] = datetime.strptime(kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if 'updated_at' not in kwargs:
                kwargs['updated_at'] = datetime.now()
            else:
                kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')

            if '__class__' in kwargs:
                del kwargs['__class__']

            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = self.__class__.__name__
        return '[{}] ({}) {}'.format(
            cls, self.id,
            self.to_dict(iso=False))

    def save(self):
        """Updates updated_at with the current time when the instance is changed"""
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self, iso=True):
        """Convert instance into a dictionary format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__': self.__class__.__name__})
        if iso:
            dictionary['created_at'] = self.created_at.isoformat()
            dictionary['updated_at'] = self.updated_at.isoformat()

        dictionary.pop('_sa_instance_state', None)
        return dictionary

    def delete(self):
        """Delete the object from storage and remove it from memory"""
        from models import storage
        storage.delete(self)
        del self


#!/usr/bin/python3
"""
This module defines a base class for all models in our hbnb clone
The class defines a base class for all models in a hbnb clone,
providing common attributes and
#methods.
"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
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
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if 'id' not in kwargs.keys():
                kwargs['id'] = str(uuid.uuid4())
            if 'created_at' not in kwargs.keys():
                kwargs['created_at'] = datetime.now()
            else:
                kwargs['created_at'] = datetime.\
                      strptime(kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if 'updated_at' not in kwargs.keys():
                kwargs['updated_at'] = datetime.now()
            else:
                kwargs['updated_at'] = datetime.\
                      strptime(kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')

            if '__class__' in kwargs.keys():
                del kwargs['__class__']

            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        my_dic = {}
        # for k, v in self.to_dict(iso=False).items():
        #     if k != '__class__':
        #         my_dic[k] = v
        return '[{}] ({}) {}'.format(
            cls, self.id,
            self.to_dict(iso=False))

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        # print("base model save")
        storage.new(self)
        storage.save()

    def to_dict(self, iso=True):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        if iso:
            dictionary['created_at'] = self.created_at.isoformat()
            dictionary['updated_at'] = self.updated_at.isoformat()

        if '_sa_instance_state' in dictionary.keys():
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """
        The delete function deletes an object from
        storage and removes it from memory.
        """
        storage.delete(self)
        del self

#!/usr/bin/python3
"""
The `Place` class represents a place to stay
in the AirBnB project
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Table
from os import getenv
from models import storage
from models.review import Review
from models.amenity import Amenity


"""
The `place_amenity` variable is creating a table called
`place_amenity` in the database. This table
"""
place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """
    The `Place` class represents a place to stay with
    various attributes such as name, description,
    number of rooms, number of bathrooms,
    maximum number of guests, price per night, latitude,
    longitude, and a list of amenity IDs.
    """

    __tablename__ = "places"
    city_id = Column(String(60),
                     ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60),
                     ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review',
                               backref='place', cascade="all, delete")
        amenities = relationship('Amenity',
                                 secondary="place_amenity",
                                 viewonly=False)
    else:
        @property
        def reviews(self):
            """
            The function "reviews" returns a list of reviews
            associated with a specific place.
            """
            my_list = []
            for i in storage.all(Review).values():
                if i.place_id == self.id:
                    my_list.append(i)
            return my_list

        @property
        def amenities(self):
            """
            The function "amenities" returns a list of amenities
            based on their IDs.
            """
            my_list = []
            for i, j in storage.all(Amenity).items():
                if i in self.amenity_ids.keys():
                    my_list.append(j)
            return my_list

        @amenities.setter
        def amenities(self, value=None):
            """
            The function "amenities" appends an Amenity object
            to a list if the input value is of type
            Amenity.
            """
            if type(value).__name__ is Amenity:
                new = "Amenity" + "." + value.id
                self.amenity_ids.append(new)

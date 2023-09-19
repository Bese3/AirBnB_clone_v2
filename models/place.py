#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")

class Place(BaseModel):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    if storage_type == 'db':
        # Define the place_amenity table for Many-To-Many
        place_amenity = Table(
            'place_amenity',
            BaseModel.metadata,
            Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
            Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
        )

        # Add the 'amenities' relationship as secondary with viewonly=False
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False,
            back_populates="place_amenities"
        )
    elif storage_type == 'file':
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.amenity_ids = []

        @property
        def amenities(self):
            """Getter attribute that returns a list of Amenity instances based on amenity_ids"""
            from models import storage
            amenity_instances = []
            for amenity_id in self.amenity_ids:
                amenity = storage.get("Amenity", amenity_id)
                if amenity:
                    amenity_instances.append(amenity)
            return amenity_instances

        @amenities.setter
        def amenities(self, value):
            """Setter attribute for amenities."""
            if isinstance(value, Amenity):
                self.amenity_ids.append(value.id)


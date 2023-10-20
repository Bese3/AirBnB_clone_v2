#!/usr/bin/python3
""" State Module for HBNB project """
from models.place import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """
    The `Amenity` class represents an amenity with a name attribute.
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    # place_amenities = relationship("Place", secondary="place_amenity",
    #                                viewonly=False)

#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class User(BaseModel):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    # Add the 'places' relationship and specify the cascade behavior
    places = relationship("Place", backref="user", cascade="all, delete-orphan")

    # Add the 'reviews' relationship and specify the cascade behavior
    reviews = relationship("Review", backref="user", cascade="all, delete-orphan")


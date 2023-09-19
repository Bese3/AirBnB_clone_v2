#!/usr/bin/python3

from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


classes = {
    'User': User,
    'State': State,
    'City': City,
    'Place': Place,
    # 'Amenity': Amenity,
    'Review': Review
}

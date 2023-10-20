#!/usr/bin/python3
""" Module for testing db storage"""
import unittest
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session
from models.engine.db_storage import DBStorage
from sqlalchemy.orm import sessionmaker
import os
from unittest.mock import patch
import MySQLdb


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'fs',
                 'Test DBStorage')
class test_DBStorage(unittest.TestCase):
    """ Class to test the fidble storage method """

    @classmethod
    def setUpClass(cls):
        """
        The setUpClass function sets up the necessary objects
        and data for testing a database storage class.
        """
        cls.storage = storage
        Base.metadata.create_all(cls.storage._DBStorage__engine)
        Session = sessionmaker(bind=cls.storage._DBStorage__engine)
        cls.storage._DBStorage__session = Session()
        cls.state = State(name="California")
        cls.storage._DBStorage__session.add(cls.state)
        cls.city = City(name="San_Jose", state_id=cls.state.id)
        cls.storage._DBStorage__session.add(cls.city)
        cls.user = User(email="poppy@holberton.com", password="betty")
        cls.storage._DBStorage__session.add(cls.user)
        cls.place = Place(city_id=cls.city.id, user_id=cls.user.id,
                          name="School")
        cls.storage._DBStorage__session.add(cls.place)
        cls.amenity = Amenity(name="Wifi")
        cls.storage._DBStorage__session.add(cls.amenity)
        cls.review = Review(place_id=cls.place.id, user_id=cls.user.id,
                            text="stellar")
        cls.storage._DBStorage__session.add(cls.review)
        cls.storage._DBStorage__session.commit()

    @classmethod
    def tearDownClass(cls):
        """
        The `tearDownClass` function is used to clean up and delete
        objects from the database after
        running tests.
        """
        cls.storage._DBStorage__session.delete(cls.state)
        # cls.storage._DBStorage__session.delete(cls.city)
        cls.storage._DBStorage__session.delete(cls.user)
        cls.storage._DBStorage__session.delete(cls.amenity)
        cls.storage._DBStorage__session.commit()
        del cls.state
        del cls.city
        del cls.user
        del cls.place
        del cls.amenity
        del cls.review
        cls.storage._DBStorage__session.close()
        del cls.storage
        # connect = MySQLdb.connect(host="localhost", port=3306,
        #                           user="hbnb_dev", passwd="hbnb_dev_pwd",
        #                           charset="utf8")
        # cur = connect.cursor()
        # cur.execute("DROP DATABASE IF EXISTS hbnb_dev_db")
        # connect.commit()
        # cur.close()

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(DBStorage.__doc__)
        self.assertIsNotNone(DBStorage.__init__.__doc__)
        self.assertIsNotNone(DBStorage.all.__doc__)
        self.assertIsNotNone(DBStorage.new.__doc__)
        self.assertIsNotNone(DBStorage.save.__doc__)
        self.assertIsNotNone(DBStorage.delete.__doc__)
        self.assertIsNotNone(DBStorage.reload.__doc__)

    def test_attribute(self):
        """
        The function tests if the attributes of the storage
        object are of the correct types.
        """
        self.assertTrue(type(self.storage._DBStorage__engine) is Engine)
        self.assertTrue(isinstance(self.storage._DBStorage__session, Session))

    def test_methods(self):
        """Check for methods."""
        self.assertTrue(hasattr(DBStorage, "__init__"))
        self.assertTrue(hasattr(DBStorage, "all"))
        self.assertTrue(hasattr(DBStorage, "new"))
        self.assertTrue(hasattr(DBStorage, "save"))
        self.assertTrue(hasattr(DBStorage, "delete"))
        self.assertTrue(hasattr(DBStorage, "reload"))

    def test_all(self):
        """Test default all method."""
        self.assertEqual(type(DBStorage.all(storage)), dict)

    def test_new(self):
        """Test new method."""
        st = State(name="Washington")
        self.storage.new(st)
        store = list(self.storage._DBStorage__session.new)
        self.assertIn(st, store)

    def test_save(self):
        """Test save method."""
        db = MySQLdb.connect(user="hbnb_dev",
                             passwd="hbnb_dev_pwd",
                             db="hbnb_dev_db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM states where binary name ='Virginia'")
        query = cursor.fetchall()
        first_length = len(query)

        st = State(name="Virginia")
        self.storage._DBStorage__session.add(st)
        self.storage.save()
        cursor.execute("SELECT * FROM states WHERE BINARY name ='Virginia'")
        my_query = cursor.fetchall()
        self.assertEqual(len(my_query), first_length)
        self.assertNotIn(st.id, my_query)
        cursor.close()

    def test_delete(self):
        """Test delete method."""
        st = State(name="New_York")
        self.storage._DBStorage__session.add(st)
        self.storage._DBStorage__session.commit()
        self.storage.delete(st)
        self.assertIn(st, list(self.storage._DBStorage__session.deleted))

    def test_reload(self):
        """Test reload method."""
        og_session = self.storage._DBStorage__session
        self.storage.reload()
        self.assertIsInstance(self.storage._DBStorage__session, Session)
        self.assertNotEqual(og_session, self.storage._DBStorage__session)
        self.storage._DBStorage__session.close()
        self.storage._DBStorage__session = og_session


if __name__ == '__main__':
    unittest.main()

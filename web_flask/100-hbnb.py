#!/usr/bin/python3
""" flask module for states"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from os import getenv
app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    The function `hbnb` retrieves data from storage and
    renders a template with sorted states,
    amenities, places and the storage type."""
    storage_type = getenv("HBNB_TYPE_STORAGE")
    all_state = storage.all(State)
    all_amenity = storage.all(Amenity)
    all_place = storage.all(Place)
    places = sorted(all_place.values(),
                    key=lambda places: places.name)
    amenities = sorted(all_amenity.values(),
                       key=lambda amenities: amenities.name)
    states = sorted(all_state.values(),
                    key=lambda states: states.name)
    return render_template("100-hbnb.html", states=states,
                           amenities=amenities,
                           storage_type=storage_type, places=places)


@app.teardown_appcontext
def close(exception):
    """
    The function `close` is used to close a storage object.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

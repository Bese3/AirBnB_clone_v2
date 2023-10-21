#!/usr/bin/python3
""" flask module for states"""
from models import storage
from flask import Flask, render_template
from models.state import State
app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """
    The function retrieves all states from storage,
    sorts them by name, and returns a rendered template
    with the sorted states."""
    all_state = storage.all(State)
    states = sorted(all_state.values(), key=lambda state: state.name)
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def close(exception):
    """
    The function `close` is used to close a storage object.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

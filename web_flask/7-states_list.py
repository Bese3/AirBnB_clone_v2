#!/usr/bin/python3
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def state_list():
    """
    The function retrieves a list of all states from storage,
    sorts them alphabetically by name, and returns the lis
    to be rendered in an HTML template.
    """
    all_states = storage.all(State)
    states = sorted(all_states.values(), key=lambda state: state.name)
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def close(excpetion):
    """
    The function `close` is used to close a storage object.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

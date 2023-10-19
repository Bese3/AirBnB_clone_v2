#!/usr/bin/python3
'''Module 0-hello_route
A basic Flask app that writes "Hello, HBNB!" to the screen
'''

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def root_route():
    """
    The function `root_route` returns the string "Hello HBNB!".
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb_route():
    """
    The function hbnb_route returns the string "HBNB".
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    text = text.replace("_", " ")
    return f"C {text}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

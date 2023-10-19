#!/usr/bin/python3
'''Module 0-hello_route
A basic Flask app that writes "Hello, HBNB!" to the screen
'''

from flask import Flask, render_template
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
    """
    The function `c_route` takes a string as input,
    replaces underscores with spaces, and returns a
    formatted string starting with "C"."""
    text = text.replace("_", " ")
    return "C {}".format(text)


@app.route('/python/', strict_slashes=False)
def python():
    """
    The function python() returns the string "Python is cool".
    """
    return "Python is cool"


@app.route('/python/<text>', strict_slashes=False)
def python_route(text):
    """
    The function `python_route` replaces underscores with spaces
    in the input text and returns a formatted string."""
    text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n: int):
    """
    The function "number_route" takes an integer as input and
    returns a string indicating that the input is a number."""
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n: int):
    """
    The function `number_template` returns the rendered template
    '5-number.html' with the variable `n` passed as an argument."""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n: int):
    """
    The function determines whether a given number is odd or even
    and returns the result along with the number itself in an HTML template."""
    e_o = "even" if n % 2 == 0 else "odd"
    return render_template('6-number_odd_or_even.html', n=n, e_o=e_o)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

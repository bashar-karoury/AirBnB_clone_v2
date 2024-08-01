#!/usr/bin/python3
""" python script to run flask application that
    return Hello HBNB! on requests to 0.0.0.0 port 5000
"""
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def HBNB():
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_is_cool(text):
    # show the user profile for that user
    return "C {}".format(text.replace('_', ' '))


@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text):
    # show the user profile for that user
    return "Python {}".format(text.replace('_', ' '))


@app.route('/python', strict_slashes=False)
def python_alone_is_cool():
    # show the user profile for that user
    return "Python is cool"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

#!/usr/bin/python3
""" python script to run flask application that
    return Hello HBNB! on requests to 0.0.0.0 port 5000
"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def HBNB():
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_is_cool(text):
    return "C {}".format(text.replace('_', ' '))


@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text):
    return "Python {}".format(text.replace('_', ' '))


@app.route('/python', strict_slashes=False)
def python_alone_is_cool():
    return "Python is cool"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

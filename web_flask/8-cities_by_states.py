#!/usr/bin/python3
""" python script to run flask application that
     list of all State objects present in DBStorage sorted by name (A->Z)
"""
from flask import Flask, render_template
from models import storage, State, City
app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def states_list():
    states = storage.all(State)
    states = list(states.values())
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def close_session(exception=None):
    """close session after each request
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

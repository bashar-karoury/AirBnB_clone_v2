#!/usr/bin/python3
""" python script to run flask application that
     list of all State objects present in DBStorage sorted by name (A->Z)
"""
from flask import Flask, render_template
from models import storage, State, City, Amenity, Place
app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def states_list():
    states = storage.all(State)
    states = list(states.values())
    amenities = list(storage.all(Amenity).values())
    places = list(storage.all(Place).values())
    return render_template('100-hbnb.html', states=states, amens= amenities, places=places)

@app.teardown_appcontext
def close_session(exception=None):
    """close session after each request
    """
    storage.close()


if __name__ == "__main__":
    places = list(storage.all(Place).values())
    print(type(places))
    print(len(places))
    print(places[1].user)
    app.run(host='0.0.0.0', port=5000)

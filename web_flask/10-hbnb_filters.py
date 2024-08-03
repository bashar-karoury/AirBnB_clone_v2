#!/usr/bin/python3
""" python script to run flask application that
     list of all State objects present in DBStorage sorted by name (A->Z)
"""
from flask import Flask, render_template
from models import storage, State, City, Amenity
app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def states_list():
    states = storage.all(State)
    states = list(states.values())
    amenities = list(storage.all(Amenity).values())
    return render_template('10-hbnb_filters.html', states=states, amens= amenities)

"""
@app.route("/states/<id>", strict_slashes=False)
def city_by_state_list(id):
    states = storage.all(State)
    key = "State.{}".format(id)
    if key in states:
        states = states[key]
    else:
        states = None
    return render_template('9-states.html', states=states, id=key)
"""

@app.teardown_appcontext
def close_session(exception=None):
    """close session after each request
    """
    storage.close()


if __name__ == "__main__":
    amenities = list(storage.all(Amenity).values())
    print(type(amenities))
    print(len(amenities))
    app.run(host='0.0.0.0', port=5000)

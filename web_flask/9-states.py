#!/usr/bin/python3
"""Starts a Flask web application.

The application listens on 0.0.0.0, port 5000.
Routes:
    /states: HTML page with a list of all State in DBStorage.
    /states/<id>: HTML page displaying the given state with <id>
"""
from models import storage
from models.state import State
from models.city import City
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<state_id>', strict_slashes=False)
def states_route(state_id=None):
    """Displays a HTML page with the states and their cities
        listed in alphabetical order"""
    states = storage.all(State)
    the_state = storage.all(State).get("State.{}".format(state_id), None)
    return render_template('9-states.html',
                           states=states,
                           a_state=the_state,
                           state_id=state_id)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")

#!/usr/bin/python3
""" a script that starts a web flask application

The application listens on 0.0.0.0 port 5000
Routes:
    /: Displays 'Hello HBNB!'
"""
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Function when called with / displays Hello HBNB"""
    return 'Hello HBNB!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

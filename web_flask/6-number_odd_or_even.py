#!/usr/bin/python3
""" a script that starts a web flask application

The application listens on 0.0.0.0 port 5000
Routes:
    /: display 'Hello HBNB!'
    /hbnb: display 'HBNB'
    /c/<text>: display “C ” followed by the value of the <text> variable
    /python/(<text>): display “Python ”, followed by the value of the text\
            variable (replace underscore _ symbols with a space ).\
            The default value of text is “is cool”
    /number/<n>: display “n is a number” only if n is an integer
    /number_template/<n>: display a HTML page only if n is an integer\
            H1 tag: “Number: n” inside the tag BODY
    /number_odd_or_even/<n>: display a HTML page only if n is an integer\
            H1 tag: “Number: n is even|odd” inside the tag BODY
"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Function called with /"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Function called with /hbnb"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Function called with /c/<text>"""
    text = text.replace('_', ' ')
    return 'C {}'.format(text)


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text='is cool'):
    """Function called with /python/<text>"""
    text = text.replace('_', ' ')
    return 'Python {}'.format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Function called with /number/<n>"""
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Function called with /number_template/<n>"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """Function called with /number_odd_or_even/<n>"""
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

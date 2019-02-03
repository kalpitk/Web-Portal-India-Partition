import sqlite3

from flask import (Flask, g, redirect, render_template, request, session,
                   url_for)

app = Flask(__name__)


@app.route("/home", methods = ['POST', 'GET'])
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.secret_key = 'sec key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)

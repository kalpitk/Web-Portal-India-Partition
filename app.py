import mysql.connector
from flask import (Flask, g, redirect, render_template, request, session,
                   url_for)

app = Flask(__name__)
app.secret_key = 'sec key'

mydb = mysql.connector.connect(
  host='localhost',
  user='root',
  password='',
  database = 'PROJECT'
)
cursor = mydb.cursor(buffered=True)

@app.route("/home", methods = ['POST', 'GET'])
def home():
  return render_template('home.html')

@app.route("/login", methods = ['POST', 'GET'])
def login():
  username = request.form['username']
  password = request.form['password']
  cursor.execute("""SELECT username, password FROM users
                  WHERE username = %s;""", (username,))
  res = cursor.fetchall()

  if cursor.rowcount == 0 :
    # No such user
    return redirect(url_for('home'), code = 401)

  if res[0][1] != password :
    # Incorrect password
    return redirect(url_for('home'), code = 401)

  session['username'] = username

  return redirect(url_for('home'))

@app.route("/logout", methods = ['POST', 'GET'])
def logout():
  session.pop('username', None)
  session.pop('moderator', None)
  session.pop('admin', None)
  return redirect(url_for('home'))

if __name__ == "__main__":
  app.config['SESSION_TYPE'] = 'filesystem'
  app.run(debug=True)

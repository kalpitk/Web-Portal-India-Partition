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


@app.route("/sign_up", methods = ['POST', 'GET'])
def sign_up():
  username = request.form['username']
  name = request.form['name']
  password = request.form['password']
  email = request.form['email']
  error = ""

  cursor.execute("""SELECT COUNT(*) FROM user WHERE username = %s;""", (username,))
  res = cursor.fetchone()[0]
  if res != 0 :
    error = "Username already exists, please try another"

  cursor.execute("""SELECT COUNT(*) FROM user WHERE email_id = %s;""", (email,))
  res = cursor.fetchone()[0]

  if res != 0 :
    error = "Email already registered, please try signing in"

  if len(password) < 1 :
    error = "Password too short"

  if len(email) == 0 :
    error = "Invalid Email"

  if len(username) == 0 :
    error = "Username too short"

  if len(error) :
    return render_template('sign_up_page.html', error = error)

  cursor.execute("""INSERT INTO user (username, name, email_id, password) VALUES (%s,%s,%s,%s)""", (username, name, email, password,))
  mydb.commit()

  return redirect(url_for('home'))


@app.route("/login", methods = ['POST', 'GET'])
def login():
  username = request.form['username']
  password = request.form['password']
  cursor.execute("""SELECT username, password, email_id, Is_Moderator, Is_Admin, contributions FROM user WHERE username = %s;""", (username,))
  res = cursor.fetchall()

  if cursor.rowcount == 0 :
    # No such user
    return redirect(url_for('home'), code = 401)

  if res[0][1] != password :
    # Incorrect password
    return redirect(url_for('home'), code = 401)

  session['username'] = username
  session['moderator'] = res[0][3]
  session['admin'] = res[0][4]

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

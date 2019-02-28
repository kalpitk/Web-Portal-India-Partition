import mysql.connector, hashlib
from flask import (Flask, g, redirect, render_template, request, session, url_for)

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

@app.route("/sign_up_page", methods = ['POST', 'GET'])
def sign_up_page():
  return render_template('sign_up_page.html')

@app.route("/login_page", methods = ['POST', 'GET'])
def login_page():
  return render_template('login_page.html')

@app.route("/index")
def index():
  return render_template('index.html')


@app.route('/profile/<user>')
def profile(user=None):
  cursor.execute("""SELECT username,name,email_id,Is_moderator,Is_admin,contributions FROM user WHERE username = %s;""", (user,))
  res = cursor.fetchall()
  cursor.execute("""SELECT post_id,namefarticle FROM post WHERE writer_username = %s;""", (user,))
  post = cursor.fetchall()
  return render_template('user.html',user=res,post=post)

@app.route('/post/<post_id>')
def post(post_id=None):
  return render_template('home.html')

@app.route("/sign_up", methods = ['POST', 'GET'])
def sign_up():
  username = request.form['username']
  name = request.form['name']
  password = hashlib.md5(request.form['password'].encode()).hexdigest()
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

  if not email:
    error = "Invalid Email"

  if not username:
    error = "Username too short"

  if not name:
    error = "Name too short"

  if error:
    return render_template('sign_up_page.html', error = error)

  cursor.execute("""INSERT INTO user (username, name, email_id, password) VALUES (%s,%s,%s,%s)""", (username, name, email, password,))
  mydb.commit()

  return redirect(url_for('home'))


@app.route("/login", methods = ['POST', 'GET'])
def login():
  username = request.form['username']
  password = hashlib.md5(request.form['password'].encode()).hexdigest()
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

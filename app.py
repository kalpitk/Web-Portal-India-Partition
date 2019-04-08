#!/usr/bin/env python
import mysql.connector, hashlib, re
from flask import (Flask, g, redirect, render_template, request, session, url_for)

app = Flask(__name__)
app.secret_key = 'sec key'
app.url_map.strict_slashes = False

mydb = mysql.connector.connect(
  host='localhost',
  user='root',
  password='',
  database = 'PROJECT'
)
cursor = mydb.cursor(buffered=True)


@app.route("/")
@app.route("/home", methods = ['POST', 'GET'])
def home():
  cursor.execute("""SELECT src_lat, src_lng, dest_lat, dest_lng, mig_id FROM migration""")
  res = cursor.fetchall()

  cursor.execute("""SELECT post_id,nameofarticle,upvotes,downvotes,content,post_time,
						     writer_username,migrated FROM post WHERE Is_Approved IS TRUE ORDER BY upvotes""")
  posts = cursor.fetchall()
  posts.reverse()

  return render_template('home.html', res = res, posts = posts)

@app.route("/sign_up_page", methods = ['POST', 'GET'])
def sign_up_page():
  return render_template('sign_up_page.html')

@app.route("/login_page", methods = ['POST', 'GET'])
def login_page():
  return render_template('login_page.html')

@app.route("/approve_post", methods = ['POST', 'GET'])
def approve_post():
  post_id = request.form.get('post_id')
  if not session.get('moderator') or post_id == None:
    return str(False)
  success = True
  try:
    cursor.execute("UPDATE post SET Is_Approved=TRUE WHERE post_id=%s;",(post_id,))
    mydb.commit()
  except:
    success = False
  return str(success)

@app.route('/profile/<user>')
def profile(user=None):
  cursor.execute("""SELECT username,name,email_id,Is_moderator,Is_admin,contributions FROM user WHERE username = %s""", (user,))
  res = cursor.fetchall()
  if len(res) == 0:
    return redirect(url_for('lost'))
  
  cursor.execute("""SELECT post_id,nameofarticle FROM post WHERE writer_username = %s AND Is_Approved IS TRUE""", (user,))
  post = cursor.fetchall()
  return render_template('user.html',user=res,post=post)

@app.route('/post/<post_id>')
def post(post_id):
  if session.get('username') is None:
	  user = ""
  else:
		user = session.get('username')

  cursor.execute("""SELECT post_id,nameofarticle,upvotes,downvotes,content,video_link,post_time, 
                  writer_username,approver_username,migrated,Is_Approved FROM post WHERE post_id = %s""", (post_id,))
  post_data = cursor.fetchall()

  if not post_data[0][9] and not session.get('moderator') and user != post_data[0][7]:
    return redirect(url_for('lost'))
  cursor.execute("""SELECT comment_id,name,comment,commented_time,is_user FROM comment WHERE post = %s""", (post_id,))
  comments = cursor.fetchall()

  cursor.execute("""SELECT src_lat,src_lng,dest_lat,dest_lng FROM migration WHERE mig_id=%s""", (post_data[0][9],))
  coord = cursor.fetchall()

  c = None
  if len(coord):
    c = coord[0]

  return render_template('postpage.html', data=post_data, comments=comments, user=user, coord=c)

@app.route('/post/<post_id>/addcomment', methods = ['POST', 'GET'])
def addcomment(post_id):
  error=""
  mycomment = request.form['mycomment']
  isUser = False
  if not mycomment:
		error="comment is empty"
  if session.get('username') is None:
		myname = request.form['myname']
		if not myname:
			error="Name cant be empty"
  else:
    isUser = True
    myname = session.get('username')
  if not error:
    cursor.execute("""INSERT INTO comment(name,comment,post,commented_time,is_user) values(%s,%s,%s,NOW(),%s)""", (myname,mycomment,post_id,isUser,))
    mydb.commit()
  return redirect(url_for('post',post_id=post_id, error=error))

@app.route('/post/<post_id>/deletecomment/<comment_id>')
def deletecomment(post_id,comment_id):
	user = session.get('username')
	if user:
		cursor.execute("""SELECT comment_id FROM comment 
			WHERE name=%s AND comment_id=%s AND post=%s AND is_user IS TRUE""", (user,comment_id,post_id,))
		if cursor.fetchall():
			cursor.execute("""DELETE FROM comment WHERE comment_id=%s AND post=%s AND is_user IS TRUE""", (comment_id,post_id,))
		mydb.commit()
	return redirect(url_for('post',post_id=post_id))

@app.route('/top_posts')
def top_posts():
  cursor.execute("""SELECT post_id,nameofarticle,upvotes,downvotes,content,post_time,
						     writer_username,migrated FROM post WHERE Is_Approved IS TRUE ORDER BY upvotes""")
  res = cursor.fetchall()
  res.reverse()
  return render_template('post_list.html', posts=res)

@app.route('/search_post')
def search_post():
  query = request.args.get('query')
  if 'query' not in request.args:
    query = ''
  query = '%' + query + '%'
  print query
  cursor.execute("""SELECT post_id,nameofarticle,upvotes,downvotes,content,post_time,
						     writer_username,migrated FROM post WHERE Is_Approved IS TRUE AND nameofarticle 
                 LIKE %s ORDER BY upvotes""", (query,))
  res = cursor.fetchall()
  res.reverse()
  return render_template('post_list.html', posts=res)

@app.route('/post_list')
def post_list():
  src_lat = request.args.get('src_lat')
  src_lng = request.args.get('src_lng')
  dest_lat = request.args.get('dest_lat')
  dest_lng = request.args.get('dest_lng')

  if src_lat == None and src_lng == None and dest_lat == None and dest_lng == None:
    cursor.execute("""SELECT post_id,nameofarticle,upvotes,downvotes,content,post_time,
						     writer_username,migrated FROM post WHERE Is_Approved IS TRUE""")
  elif src_lat != None and src_lng != None and dest_lat == None and dest_lng == None:
    cursor.execute("""SELECT post_id,nameofarticle,upvotes,downvotes,content,post_time,
						        writer_username,migrated FROM post INNER JOIN migration 
                    ON migrated = mig_id WHERE Is_Approved IS TRUE AND ((src_lat LIKE %s And src_lng LIKE %s) OR 
                    (dest_lat LIKE %s And dest_lng LIKE %s))""", (src_lat, src_lng,src_lat, src_lng,))
  elif src_lat == None and src_lng == None and dest_lat != None and dest_lng != None:
    cursor.execute("""SELECT post_id,nameofarticle,upvotes,downvotes,content,post_time,
						       writer_username,migrated FROM post INNER JOIN migration 
                   ON migrated = mig_id WHERE Is_Approved IS TRUE AND ((src_lat LIKE %s And src_lng LIKE %s) OR 
                   (dest_lat LIKE %s And dest_lng LIKE %s))""", (dest_lat, dest_lng,dest_lat, dest_lng,))
  elif src_lat != None and src_lng != None and dest_lat != None and dest_lng != None:
    cursor.execute("""SELECT post_id,nameofarticle,upvotes,downvotes,content,post_time,
						       writer_username,migrated FROM post INNER JOIN migration 
                   ON migrated = mig_id WHERE Is_Approved IS TRUE AND src_lat LIKE %s 
                   And src_lng LIKE %s AND dest_lat LIKE %s And dest_lng LIKE %s""", (src_lat,src_lng,dest_lat, dest_lng,))
  else:
    return redirect(url_for('lost'))

  res = cursor.fetchall()
  res.reverse()
  return render_template('post_list.html', posts=res)

@app.route('/dashboard')
def dashboard():
  if session.get('username') is None:
    return redirect(url_for('lost'))
  user = session.get('username')
  cursor.execute("""SELECT post_id,nameofarticle,upvotes,downvotes,content,post_time,
		                writer_username,migrated,Is_Approved FROM post WHERE writer_username = %s""", (user,))
  posted_list = cursor.fetchall()
  cursor.execute("""SELECT Is_Moderator,Is_Admin FROM user WHERE username = %s""", (user,))
  me = cursor.fetchall()

  if not me[0][0] and not me[0][1]:
		return render_template('dashboard.html', data=posted_list, user=user, ismod=False, isadmin=False)
  if me[0][0] :
		cursor.execute("""SELECT post_id,nameofarticle,upvotes,downvotes,content,post_time,
						writer_username,migrated FROM post 
						WHERE Is_Approved= FALSE""")
		unapproved_list= cursor.fetchall()
		if not me[0][1]:
			return render_template('dashboard.html', data=posted_list, user=user,
							unapproved_list=unapproved_list, ismod=True, isadmin=False)
		else:
			cursor.execute("""SELECT username,name,email_id,contributions FROM user
					 WHERE Is_Moderator = TRUE AND Is_Admin= FALSE""")
			moderators_list=cursor.fetchall()
			return render_template('dashboard.html', data=posted_list, user=user,
					unapproved_list=unapproved_list, mods=moderators_list, ismod=True, isadmin=True)

@app.route('/dashboard/delmod/<username>')
def removeMod(username):
	if session.get('admin'):
		cursor.execute("""UPDATE user SET Is_Moderator=FALSE WHERE username=%s""", (username,))
		mydb.commit()
	return redirect(url_for('dashboard'))

@app.route("/sign_up", methods = ['POST', 'GET'])
def sign_up():
  username = request.form['username']
  name = request.form['name']
  password = hashlib.md5(request.form['password'].encode()).hexdigest()
  email = request.form['email']
  error = ""

  cursor.execute("""SELECT COUNT(*) FROM user WHERE username = %s""", (username,))
  res = cursor.fetchone()[0]
  if res != 0 :
    error = "Username already exists, please try another"

  cursor.execute("""SELECT COUNT(*) FROM user WHERE email_id = %s""", (email,))
  res = cursor.fetchone()[0]

  if res != 0 :
    error = "Email already registered, please try signing in"

  if not email:
    error = "Invalid Email"

  if not username:
    error = "Username too short"

  if not name:
    error = "Name too short"

  if any(re.findall(r'#|<|>|%', username)):
    error = "Username cannot contain special characters"

  if error:
    return render_template('sign_up_page.html', error = error)

  cursor.execute("""INSERT INTO user (username, name, email_id, password) VALUES (%s,%s,%s,%s)""", (username, name, email, password,))
  mydb.commit()

  return redirect(url_for('dashboard'))


@app.route("/login", methods = ['POST', 'GET'])
def login():
  username = request.form['username']
  password = hashlib.md5(request.form['password'].encode()).hexdigest()
  cursor.execute("""SELECT username, password, email_id, Is_Moderator, Is_Admin, contributions FROM user WHERE username = %s""", (username,))
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

  return redirect(url_for('dashboard'))

@app.route("/lost", methods = ['POST', 'GET'])
def lost():
  return render_template('lost.html')

@app.route("/logout", methods = ['POST', 'GET'])
def logout():
  session.pop('username', None)
  session.pop('moderator', None)
  session.pop('admin', None)
  return redirect(url_for('home'))

if __name__ == "__main__":
  app.config['SESSION_TYPE'] = 'filesystem'
  app.run(debug=True)

# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = 'database/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_main():
    return render_template('main_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_main'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_main'))

@app.route('/profile')
def show_profile():
    cur = g.db.execute('SELECT username, user_id, post_count, follower_count, following_count, loop_count, like_count FROM vine_page_test')
    profiles = [dict(username=row[0], user_id=row[1], post_count=row[2], follower_count=row[3], following_count=row[4], loop_count=row[5], like_count=row[6]) for row in cur.fetchall()]
    return render_template('show_profile.html', profiles=profiles)

@app.route('/profile_query', methods=['GET', 'POST'])
def profile_query():
    error = None
    if request.method == 'POST':
        profile_username = request.form['username']
        cur = g.db.execute('SELECT username, user_id, post_count, follower_count, following_count, loop_count, like_count FROM vine_page_test WHERE username = ?', [profile_username])
        profiles = [dict(username=row[0], user_id=row[1], post_count=row[2], follower_count=row[3], following_count=row[4], loop_count=row[5], like_count=row[6]) for row in cur.fetchall()]
        return render_template('show_profile.html', profiles=profiles)
    return render_template('show_profile_query.html', error=error)

@app.route('/post')
def show_post():
    cur = g.db.execute('SELECT username, created, likes, reposts, loops, comments, description, video_link, revine_check, revined_user FROM vine_post_test')
    posts = [dict(username=row[0], created=row[1], likes=row[2], reposts=row[3], loops=row[4], comments=row[5], description=row[6], video_link=row[7], revine_check=row[8], revined_user=row[9]) for row in cur.fetchall()]
    return render_template('show_post.html', posts=posts)

@app.route('/post_query', methods=['GET', 'POST'])
def post_query():
    error = None
    if request.method == 'POST':
        post_username = request.form['username']
        cur = g.db.execute('SELECT username, created, likes, reposts, loops, comments, description, video_link, revine_check, revined_user FROM vine_post_test WHERE username = ?', [post_username])
        posts = [dict(username=row[0], created=row[1], likes=row[2], reposts=row[3], loops=row[4], comments=row[5], description=row[6], video_link=row[7], revine_check=row[8], revined_user=row[9]) for row in cur.fetchall()]
        return render_template('show_post.html', posts=posts)
    return render_template('show_post_query.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0')


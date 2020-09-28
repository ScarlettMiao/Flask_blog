import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ZStack is a cool company.'

#create database connection and return it
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row #have name-based access to columns
    return conn
    
def get_post(post_id): #post_id, determines what blog post to return
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone() #fetchone() method to get the result and store it in the post variable
    conn.close()
    if post is None:
        abort(404)
    return post
    
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/')
def index():
    # return render_template('index.html')
    conn = get_db_connection()
    # the fetchall() method to fetch all the rows of the query result, this will return a list of the posts you inserted into the database
    posts = conn.execute('SELECT * FROM posts').fetchall() #execute an SQL query to select all entries from the posts table
    conn.close() #close the database connectio
    return render_template('index.html', posts=posts)# pass the posts object as an argument, which contains the results got from the database
    
#creates a /create route that accepts both GET and POST requests
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                     (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
            
    return render_template('create.html')
    
#editing an existing post, similar to creating a new one.
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)
    
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))



import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session

# Сreate Flask app, __name__ tells Flask where to look for templates folder
app = Flask(__name__)

# Secret key is used to encrypt session cookies
# In production this should be a long random string stored in environment variables
app.secret_key = 'supersecretkey'

# Admin credentials - hardcoded for simplicity
# In a real app these would be stored in a database with hashed passwords
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password123'

# Directory where article JSON files are stored
ARTICLES_DIR = 'articles'

# This function reads all the articles from the folder and returns them as a list
def get_all_articles():
    articles = []
    # os.listdir() returns a list of all filenames in the directory as strings
    # e.g. ['1.json', '2.json'] - just names, no paths or file contents
    # see notes: python os module - working with directories
    for filename in os.listdir(ARTICLES_DIR):
        if filename.endswith('.json'):
            # json.load() reads the file and converts it to a Python dictionary
            # then we append it to the list - note: all articles are loaded into memory at once
            # this is fine for a small blog but would be a problem with thousands of articles
            # in a real app we would use a database with pagination instead
            with open(f'{ARTICLES_DIR}/{filename}', encoding='utf-8') as f:
                articles.append(json.load(f))
    # Sort articles by date first, then by created_at if dates are equal
    # reverse=True means newest articles appear at the top
    # lambda x is a short anonymous function where x is a single article dictionary
    return sorted(articles, key=lambda x: (x['date'], x['created_at']), reverse=True)

def get_article(article_id):
    filepath = f'{ARTICLES_DIR}/{article_id}.json'
    # Check if article exists before opening
    # Returns None if not found so the route handler can show a 404 page
    # see notes: python os module - working with files
    if not os.path.exists(filepath):
        return None
    with open(filepath, encoding='utf-8') as f:
        return json.load(f)

def admin_required():
    # if 'admin' key is not in session - user is not logged in
    # return a redirect to login page, otherwise return None to allow access
    # see notes: Flask session
    if not session.get('admin'):
        return redirect(url_for('login'))
    return None

@app.route('/')
def home():
    articles = get_all_articles()
    # render_template() loads the HTML template and passes data to it
    # you can pass as many variables as you want: render_template('home.html', x=x, y=y)
    return render_template('home.html', articles=articles)

@app.route('/article/<int:article_id>')
def article(article_id):
    article = get_article(article_id)
    if article is None:
        # Flask accepts (template, status_code) as a return value
        # by default all routes return 200 (OK), but here we explicitly return 404 (Not Found)
        # this tells browsers and search engines that the page does not exist so they don't cache or index it
        return render_template('404.html'), 404
    return render_template('article.html', article=article)

@app.route('/login', methods=['GET', 'POST']) # register URL /length, accept GET (open page) and POST (submit form)
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            # url_for() generates a URL by function name instead of hardcoding '/admin'
            # if the route path changes, url_for() will automatically find the new path
            return redirect(url_for('admin_dashboard'))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    # session.pop() removes the 'admin' key from the session - this logs the user out
    # None is the default value if 'admin' key doesn't exist, prevents an error
    session.pop('admin', None)
    return redirect(url_for('home'))

@app.route('/admin')
def admin_dashboard():
    check = admin_required()
    # admin_required() returns a redirect to login if not logged in, None if logged in
    if check:
        return check
    articles = get_all_articles()
    return render_template('admin/dashboard.html', articles=articles)

@app.route('/admin/add', methods=['GET', 'POST'])
def admin_add():
    check = admin_required()
    if check:
        return check
    if request.method == 'POST':
        articles = get_all_articles()
        new_id = max([a['id'] for a in articles], default=0) + 1
        article = {
            'id': new_id,
            'title': request.form['title'],
            'content': request.form['content'],
            'date': datetime.now().strftime('%Y-%m-%d'),
            'created_at': datetime.now().isoformat()
        }
        with open(f'{ARTICLES_DIR}/{new_id}.json', 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2, ensure_ascii=False)
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/add.html')

@app.route('/admin/edit/<int:article_id>', methods=['GET', 'POST'])
def admin_edit(article_id):
    check = admin_required()
    if check:
        return check
    article = get_article(article_id)
    if request.method == 'POST':
        article['title'] = request.form['title']
        article['content'] = request.form['content']
        with open(f'{ARTICLES_DIR}/{article_id}.json', 'w', encoding='utf-8') as f:
            json.dump(article, f, indent=2, ensure_ascii=False)
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/edit.html', article=article)

@app.route('/admin/delete/<int:article_id>')
def admin_delete(article_id):
    check = admin_required()
    if check:
        return check
    os.remove(f'{ARTICLES_DIR}/{article_id}.json')
    return redirect(url_for('admin_dashboard'))

# only runs when starting the app directly with 'python app.py'
# on a real server (gunicorn) this block is never executed
# so debug=True/False here does not matter for production - contrary to what I thought before
if __name__ == '__main__':
    app.run(debug=True)
# Python `os` module

The `os` module is a built-in Python library for interacting with the operating system.
It lets you work with files, directories, and system processes.
```python
import os
```

---

## Working with Directories
```python
os.listdir('articles')        # Returns a list of all files/folders in a directory
os.mkdir('new_folder')        # Creates a new directory
os.makedirs('a/b/c')          # Creates nested directories (a, then b inside a, then c inside b)
os.rmdir('folder')            # Deletes an empty directory
os.getcwd()                   # Returns current working directory (e.g. 'C:/Users/you/blog')
os.chdir('/some/path')        # Changes current working directory
```

---

## Working with Files
```python
os.remove('file.json')        # Deletes a file
os.rename('old.json', 'new.json')  # Renames a file
os.path.exists('file.json')   # Returns True if file/folder exists, False if not
os.path.isfile('file.json')   # Returns True if it's a file (not a folder)
os.path.isdir('articles')     # Returns True if it's a directory (not a file)
```

---

## Working with Paths
```python
os.path.join('articles', '1.json')     # Joins path parts correctly → 'articles/1.json'
os.path.basename('articles/1.json')    # Returns filename only → '1.json'
os.path.dirname('articles/1.json')     # Returns directory only → 'articles'
os.path.splitext('1.json')             # Splits name and extension → ('1', '.json')
```

> **Note:** Always use `os.path.join()` instead of manually writing `'articles/' + filename`
> because it handles path separators correctly on Windows (`\`) and Mac/Linux (`/`).

---

## Environment Variables
```python
os.environ.get('SECRET_KEY')            # Gets an environment variable (returns None if not set)
os.environ.get('SECRET_KEY', 'default') # Returns 'default' if variable is not set
```

> **Why this matters:** In real projects you never hardcode passwords or secret keys in code.
> Instead you store them as environment variables and read them with `os.environ.get()`.

---

## Practical Example: How we use os in our blog
```python
# Get all files in the articles folder
for filename in os.listdir('articles'):
    if filename.endswith('.json'):
        # process file...

# Delete an article file
os.remove(f'articles/{article_id}.json')

# Check if an article exists before reading it
if os.path.exists(f'articles/{article_id}.json'):
    # read file...
```

---

## Summary

| Method | What it does |
|---|---|
| `os.listdir(path)` | List all files in a directory |
| `os.mkdir(path)` | Create a directory |
| `os.remove(path)` | Delete a file |
| `os.rename(old, new)` | Rename a file |
| `os.getcwd()` | Get current directory |
| `os.path.exists(path)` | Check if file/folder exists |
| `os.path.join(...)` | Safely join path parts |
| `os.environ.get(key)` | Read environment variable |

---

# Flask `session`

`session` is a dictionary-like object that stores data between requests for a specific user.
Flask encrypts it and stores it in a cookie in the browser.
Requires `app.secret_key` to be set.
```python
from flask import session
```

---

## Common methods
```python
session['admin'] = True        # Set a value
session.get('admin')           # Get a value (returns None if not found)
session.get('admin', False)    # Get a value with a default
session.pop('admin', None)     # Remove a value
session.clear()                # Clear all session data
'admin' in session             # Check if key exists
```

---

## How we use it in our blog
```python
# On login - save admin status
session['admin'] = True

# On each admin page - check if logged in
session.get('admin')  # returns True if logged in, None if not

# On logout - remove admin status
session.pop('admin', None)
```

---

## Important notes

- Session data is stored in the browser as an encrypted cookie
- The encryption uses `app.secret_key` - without it sessions won't work
- Session is cleared when the browser is closed (by default)
- Never store sensitive data like passwords in the session

---

# Jinja2 Templates

Jinja2 is a templating engine built into Flask.
It adds loops, conditions, and functions to HTML templates on the server side.
Flask processes the template and returns plain HTML to the browser.
```
Jinja2 template → Flask processes on server → plain HTML → browser
```

The key difference from JavaScript: Jinja2 runs on the **server** before the page is sent,
JavaScript runs on the **client** after the page is loaded in the browser.

---

## Syntax
```html
{{ variable }}               <!-- output a variable -->
{{ article.title }}          <!-- access dictionary key -->
{{ article.content[:120] }}  <!-- slice a string -->

{% if error %}               <!-- condition -->
{% endif %}

{% for article in articles %}  <!-- loop -->
{% endfor %}

{% extends 'base.html' %}      <!-- inherit from another template -->
{% block content %}            <!-- define a block that child templates can fill -->
{% endblock %}
```

---

## Template Inheritance

`base.html` contains the shared layout (header, footer, CSS link).
Other templates extend it and only define their own content.
```html
<!-- base.html -->
<header>...</header>
<main>
    {% block content %}{% endblock %}  <!-- placeholder for child content -->
</main>

<!-- home.html -->
{% extends 'base.html' %}
{% block content %}
    <h1>Articles</h1>   <!-- this goes into the placeholder -->
{% endblock %}
```

---

## url_for() in templates
```html
<!-- generate a URL by function name -->
<a href="{{ url_for('home') }}">Home</a>
<a href="{{ url_for('article', article_id=1) }}">Article</a>  <!-- → /article/1 -->

<!-- link to static files -->
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
```

---

## Forms and request.form
```html
<!-- HTML form sends POST request to the server -->
<form method="POST">
    <input type="text" name="title">   <!-- 'name' attribute is the key in request.form -->
    <button type="submit">Save</button>
</form>
```
```python
# Flask reads form data with request.form
title = request.form['title']
```

---

## Passing data from Flask to templates
```python
# Flask
render_template('home.html', articles=articles, user='John')
```
```html
<!-- template -->
{{ articles }}   <!-- the list -->
{{ user }}       <!-- 'John' -->
```

Left side of `=` is the variable name in the template, right side is the data from Python.
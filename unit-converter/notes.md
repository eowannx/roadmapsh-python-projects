## Flask

Flask is a lightweight web framework for Python.
```python
pip install flask
from flask import Flask, render_template, request, redirect, url_for
```

## Setup
```python
app = Flask(__name__)  # create Flask app, __name__ tells Flask where to look for templates folder
```

## Routes

Routes define which function handles which URL.
Decorator `@app.route` registers the URL and accepted HTTP methods.
```python
@app.route("/length", methods=["GET", "POST"])
def length():
    ...
```

### HTTP methods
- `GET` - user opens the page in browser
- `POST` - user submits a form
```python
if request.method == "POST":  # check if form was submitted
    value = request.form["value"]       # get form field by name attribute
    from_unit = request.form["from_unit"]
```

## render_template

Renders an HTML file from the `templates` folder and passes variables to it.
Variables are accessible in HTML via `{{ variable_name }}`.
```python
return render_template("length.html", result=result, error=error, units=list(LENGTH_TO_METERS.keys()))
#                       ^ html file    ^ variable name = value passed to HTML
```

## redirect and url_for

`redirect` sends the browser to a different URL.
`url_for` generates URL by function name instead of hardcoding the path.
```python
return redirect(url_for("length"))  # redirects to /length route
```

Using `url_for` is better than hardcoding `"/length"` because if you change the route path,
`url_for` updates automatically — hardcoded string would break.

## Running the server
```python
if __name__ == "__main__":
    app.run(debug=True)   # development: auto-restart, detailed errors in browser
    app.run(debug=False)  # production: hides internal code from users
```

## Project structure

Flask requires HTML templates to be in a `templates` folder next to `app.py`:
```
project/
├── app.py
└── templates/
    ├── length.html
    ├── weight.html
    └── temperature.html
```

---

## HTML + Flask (Jinja2)

Jinja2 is a templating engine built into Flask.
It allows using Python-like logic directly in HTML files.
Templates must be placed in the `templates` folder next to `app.py`.

## Jinja2 syntax
```html
{{ variable }}               <!-- output variable passed from render_template -->
{{ variable.capitalize() }}  <!-- can call Python string methods directly -->

{% if result is not none %}  <!-- condition block (note: none is lowercase in Jinja2, not None) -->
...
{% endif %}                  <!-- must always close if block -->

{% for unit in units %}      <!-- loop block -->
...
{% endfor %}                 <!-- must always close for block -->
```

## Critical: form field names must match request.form keys in Python
```html
<!-- HTML -->
<input name="value">
<select name="from_unit">
<select name="to_unit">
```
```python
# Python - must match exactly
request.form["value"]
request.form["from_unit"]
request.form["to_unit"]
```

Mismatch between HTML name and Python key causes KeyError.

## Critical: form method and action must match route in app.py
```html
<form method="POST" action="/length">
```
```python
@app.route("/length", methods=["GET", "POST"])
```

- `method="POST"` must match methods list in route
- `action="/length"` must match route URL

## Navigation links
```html
<a href="/length" class="active">Length</a>  <!-- class="active" highlights current page -->
<a href="/weight">Weight</a>
<a href="/temperature">Temperature</a>
```

Links use Flask route URLs directly — same as defined in `@app.route`.
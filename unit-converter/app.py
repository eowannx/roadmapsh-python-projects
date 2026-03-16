from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__) # create Flask app, __name__ tells Flask where to look for templates folder

# Length conversions (in meters to target)
LENGTH_TO_METERS = {
    "millimeter": 0.001,
    "centimeter": 0.01,
    "meter": 1.0,
    "kilometer": 1000.0,
    "inch": 0.0254,
    "foot": 0.3048,
    "yard": 0.9144,
    "mile": 1609.344,
}

# Weight conversions (in grams to target)
WEIGHT_TO_GRAMS = {
    "milligram": 0.001,
    "gram": 1.0,
    "kilogram": 1000.0,
    "ounce": 28.3495,
    "pound": 453.592,
}


def convert_length(value, from_unit, to_unit):
    in_meters = value * LENGTH_TO_METERS[from_unit]
    return in_meters / LENGTH_TO_METERS[to_unit]


def convert_weight(value, from_unit, to_unit):
    in_grams = value * WEIGHT_TO_GRAMS[from_unit]
    return in_grams / WEIGHT_TO_GRAMS[to_unit]


def convert_temperature(value, from_unit, to_unit):
    # Convert to Celsius first
    if from_unit == "fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "kelvin":
        celsius = value - 273.15
    else:
        celsius = value

    # Convert from Celsius to target
    if to_unit == "fahrenheit":
        return celsius * 9 / 5 + 32
    elif to_unit == "kelvin":
        return celsius + 273.15
    else:
        return celsius


@app.route("/length", methods=["GET", "POST"]) # register URL /length, accept GET (open page) and POST (submit form)
def length():
    result = None # no result until form is submitted
    error = None  # no error until something goes wrong

    if request.method == "POST": # form submitted, calculate result
        try:
            value = float(request.form["value"])
            from_unit = request.form["from_unit"]
            to_unit = request.form["to_unit"]
            result = round(convert_length(value, from_unit, to_unit), 6)
        except (ValueError, KeyError): # catches invalid input bypassing HTML validation (e.g. via Postman)
            error = "Invalid input. Please enter a valid number."

    # pass result, error and unit list to HTML template
    return render_template("length.html", result=result, error=error,
                           units=list(LENGTH_TO_METERS.keys()))


@app.route("/weight", methods=["GET", "POST"])  # register URL /weight, accept GET (open page) and POST (submit form)
def weight():
    result = None  # no result until form is submitted
    error = None   # no error until something goes wrong

    if request.method == "POST":  # form submitted, calculate result
        try:
            value = float(request.form["value"])
            from_unit = request.form["from_unit"]
            to_unit = request.form["to_unit"]
            result = round(convert_weight(value, from_unit, to_unit), 6)
        except (ValueError, KeyError):  # catches invalid input bypassing HTML validation (e.g. via Postman)
            error = "Invalid input. Please enter a valid number."

    # pass result, error and unit list to HTML template
    return render_template("weight.html", result=result, error=error,
                           units=list(WEIGHT_TO_GRAMS.keys()))


@app.route("/temperature", methods=["GET", "POST"])  # register URL /temperature, accept GET (open page) and POST (submit form)
def temperature():
    result = None  # no result until form is submitted
    error = None   # no error until something goes wrong

    if request.method == "POST":  # form submitted, calculate result
        try:
            value = float(request.form["value"])
            from_unit = request.form["from_unit"]
            to_unit = request.form["to_unit"]
            result = round(convert_temperature(value, from_unit, to_unit), 6)
        except (ValueError, KeyError):  # catches invalid input bypassing HTML validation (e.g. via Postman)
            error = "Invalid input. Please enter a valid number."

    # pass result, error and unit list to HTML template
    return render_template("temperature.html", result=result, error=error,
                           units=["celsius", "fahrenheit", "kelvin"])


@app.route("/")
def index():
    # redirect to /length instead of rendering length.html directly here
    # direct render would mean two routes showing the same content (redundant)
    return redirect(url_for("length"))

# This block executes only if file executed directly
# (and not imported as a module in another file)
if __name__ == "__main__":
    # debug=True for development: auto-restart on code changes, detailed errors in browser
    # debug=False for production: hides internal code from users
    app.run(debug=False)
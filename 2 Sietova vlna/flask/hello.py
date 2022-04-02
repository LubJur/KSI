from math import factorial as fact
from flask import Flask, request, url_for, abort
app = Flask("Factorial")

@app.route("/factorial", methods=["POST", "GET"])
def factorial():

    if request.method == "GET":
        return "<p>Hello world</p>"
    try:
        n = int(request.form["number"])
        return f"""<form action="{url_for('factorial')}" method="post">
        Enter number: <input type="text" name="number">
        <br><input type="submit"></form>"""
    except (KeyError, ValueError):
        abort(400)

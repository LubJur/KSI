from flask import Flask, request, url_for, abort, jsonify, render_template, escape, redirect
import requests
from json import loads
from datetime import datetime
import time

app = Flask("webserver_test")
app.secret_key = "dasdasdasdasd"

"""
@app.route("/post", methods=["POST", "GET"])
def funk():
    result = request.form
    if request.method == "GET":
        print("data", result)
        try:
            username = result.getlist("username")[0]
            password = result.getlist("password")[0]
            print("data", username)
            print("data", password)
            return f"{{ username }} {{ password }}"
        except IndexError:  # if you get to the site by url only
            return "Invalid user"
        return result
    elif request.method == "POST":
        pass
"""
session = {}

@app.route("/")
def index():
    print(session)
    if "username" in session:
        username = session["username"]
        return "Logged in as " + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
    else:
        return "You are not logged in <br><a href = '/login'>" + "click here to log in</a>"

@app.route("/login", methods=["GET", "POST"])
def login():
    print("som tu")
    print(request.method)
    if request.method == "POST":
        session["username"] = request.form["username"]
        print(session)
        return redirect("/")
    print(session)
    return '''
    <form action="" method="post">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit">
    </form>
'''

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

from flask import Flask, request, url_for, abort, jsonify, render_template, escape
import requests
from json import loads
from datetime import datetime
import time

app = Flask("webserver_test")

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
            return f"""{{ username }} {{ password }}"""
        except IndexError:  # if you get to the site by url only
            return "Invalid user"
        return result
    elif request.method == "POST":
        pass

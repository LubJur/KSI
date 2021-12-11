from flask import Flask, request, url_for, abort, jsonify, render_template, escape, redirect
import requests
from json import loads
from datetime import datetime
import time
from suntime import Sun

app = Flask("webserver")
app.secret_key = "3FauQvwhSo4mpcc"
motion_id = {"obyvakMotion": 0, "kuchyneMotion": 0}
for sensor in motion_id:
    print(sensor)
    get_response = requests.get("https://home_automation.iamroot.eu/newMotionSensor")
    id = loads(get_response.text)["id"]
    motion_id.update({sensor: id})

print(motion_id)

get_response = requests.get("https://home_automation.iamroot.eu/device/")


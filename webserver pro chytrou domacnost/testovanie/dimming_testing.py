from flask import Flask, request, url_for, abort, jsonify, render_template, escape, redirect
import requests
from json import loads
from datetime import datetime
import time
from suntime import Sun

app = Flask("webserver")
app.secret_key = "3FauQvwhSo4mpcc"

session = {}
lights_id = {"obyvakLight": 0, "koupelnaLight": 0, "kuchyneLight": 0, "karsobLight": 0, "karlikLight": 0,
             "karlosLight": 0, "juliaLight": 0}
light_status = {}
switches_id = {"obyvakSwitch": 0, "koupelnaSwitch": 0, "kuchyneSwitch": 0, "karsobSwitch": 0, "karlikSwitch": 0,
               "karlosSwitch": 0, "juliaSwitch": 0}
motion_id = {"obyvakMotion": 0, "kuchyneMotion": 0}
"""
for light in lights_id:
    print(light)
    get_response = requests.get("https://home_automation.iamroot.eu/newSmartLight")
    id = loads(get_response.text)["id"]
    lights_id.update({light: id})
    light_status[lights_id[light]] = loads(get_response.text)["current_state"]
    print(light_status)
"""
# zmena farby svetla podla casu
@app.route("/cron")
def change_color():
    # https://pypi.org/project/suntime/
    change_needed = False
    sun = Sun(48.749167, 21.901389)
    sunset = sun.get_sunset_time()
    sunset = int(sunset.strftime("%H")) * 60 + int(sunset.strftime("%M"))
    sunrise = sun.get_sunrise_time()
    sunrise = int(sunrise.strftime("%H")) * 60 + int(sunrise.strftime("%M"))
    now_time = datetime.now().time()  # https://www.programiz.com/python-programming/datetime/current-time
    now_time = int(now_time.strftime("%H")) * 60 + int(now_time.strftime("%M")) # hours * 60 + minutes so we can only work in minutes

    if sunset + 90 >= now_time >= sunset:  # when now_time is after sunset  6500 -> 2300
        change_needed = True
        # starting_color - ((now_time - sunset) * change_in_minute)
        color = 6500 - ((now_time - sunset) * (4200/90))

    elif sunrise >= now_time >= sunrise - 90:
        change_needed = True
        # (now_time - (sunrise - 90 min)) * change_in_minute + starting_color
        color = (now_time - (sunrise - 90)) * (4200/90) + 2300

    if change_needed:
        for light in lights_id:
            id = lights_id[light]
            time.sleep(0.2)
            get_response = requests.get(
                f"https://home_automation.iamroot.eu/device/{id}/color_temperature/{color}")

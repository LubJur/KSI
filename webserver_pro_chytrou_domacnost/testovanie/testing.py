import requests  # python -m pip install -U requests
from time import sleep
from flask import Flask, render_template
import numpy as np

"""@app.route("/newSmartLight")
def newSmartLight():
    #if request.method == "GET":
    uuid = uuid4()
    print(uuid)
    answer = {
        "actions": {
            "change_color_blue_sky": f"http://localhost:5000/device/{uuid}/color_temperature/10000",
            "change_color_high_noon": f"http://localhost:5000/device/{uuid}/color_temperature/5000",
            "change_color_sunset": f"http://localhost:5000/device/{uuid}/color_temperature/3500",
            "device_info": f"http://localhost:5000/device/{uuid}",
            "set_notes_POST": f"http://localhost:5000/device/{uuid}/notes",
            "toggle_state": f"http://localhost:5000/device/{uuid}/toggle",
            "turn_off": f"http://localhost:5000/device/{uuid}/state/off",
            "turn_on": f"http://localhost:5000/device/{uuid}/state/on"
        },
        "color_temperature": 5000,
        "current_state": False,
        "id": uuid,
        "notes": "",
        "power_usage": 0,
        "power_usage_coefficient": 100,
        "power_usage_last_recalculated": 0,
        "type": "SmartLight"
    }
    return jsonify(answer)

@app.route("/newMotionSensor")
def newMotionSensor():
    uuid = uuid4()
    answer = {
        "actions": {
            "change_report_url": f"http://localhost:5000/device/{uuid}/report_url?url=http%3A%2F%2Fhome_automation.iamroot.eu%2Fdevice%2Fb28cd825-0fbc-483b-b22c-5b27e4d85c79%2Fevent",
            "device_info": f"http://localhost:5000/device/{uuid}",
            "set_notes_POST": f"http://localhost:5000/device/{uuid}/notes",
            "trigger_report": f"http://localhost:5000/device/{uuid}/trigger"
        },
        "collector_url": f"http://localhost:5000/device/{uuid}/event",
        "id": uuid,
        "last_triggered_timestamp": 0,
        "notes": "",
        "type": "MotionSensor"
    }
    return jsonify(answer)

@app.route("/newSwitchSensor")
def newSwitchSensor():
    uuid = uuid4()
    answer = {
        "actions": {
            "change_report_url": f"http://localhost:5000/device/{uuid}/report_url?url=http%3A%2F%2Fhome_automation.iamroot.eu%2Fdevice%2F4dfe3f5a-8d40-44d5-b33b-c110c07a92a3%2Fevent",
            "device_info": f"http://localhost:5000/device/{uuid}",
            "set_notes_POST": f"http://localhost:5000/device/{uuid}/notes",
            "trigger_report": f"http://localhost:5000/device/{uuid}/trigger"
        },
        "collector_url": f"http://localhost:5000/device/{uuid}/event",
        "current_state": False,
        "id": uuid,
        "notes": "",
        "power_usage": 0,
        "power_usage_coefficient": 100,
        "power_usage_last_recalculated": 1637265681,
        "type": "SwitchSensor"
    }
    return jsonify(answer)


data = {"username": "Karlik", "password": "Karlikpass"}
post_response = requests.get("http://127.0.0.1:5000/map", data=data)
print(post_response)
"""
#get_response = requests.get("http://home_automation.iamroot.eu/newSwitchSensor")
#print(get_response.text)


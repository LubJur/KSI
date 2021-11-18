import requests  # python -m pip install -U requests
from time import sleep

get_response = requests.get("http://localhost:5000/newSmartLight")
print(get_response.text)

get_response = requests.get("http://localhost:5000/newMotionSensor")
print(get_response.text)

get_response = requests.get("http://localhost:5000/newSwitchSensor")
print(get_response.text)

#get_response = requests.get("http://home_automation.iamroot.eu/newSwitchSensor")
#print(get_response.text)
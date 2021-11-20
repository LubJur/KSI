# TODO: Automatizacia
# TODO: automaticke zapinanie svetla kuchyne a chodby podla senzora pohybu
# TODO: Pri zapade slnka 6500K -> 2300K, pri vychode naopak, 47K za minutu pocas pol hodiny https://michelanders.blogspot.com/2010/12/calulating-sunrise-and-sunset-in-python.html
# TODO: Ovladanie svetiel pomocou smart vypinacou priamo, bez servera
# TODO: Vzdialene vypinanie svetiel v miestnosti (nie ale v rozdielnych izbach)
# TODO: rozdelenie ceny za plyn podla toho ako dlho v ich izbe svietilo svetlo

# TODO: Webstranky
# TODO: mapa bytu s informaciami ake svetla su zasvietene a aku maju farbu
# TODO: Tabulka s odkazmi na zariadenia, v ktorej miestnosti su (odkaz ide cez server)
# TODO: prehlad kolko percent ceny plynu by mal kto zaplatit
# TODO: formular cez ktory sa mozu spolubyvajuci prihlasit
# TODO: zoznam s tlacidlami na ovladanie svetiel pre kazdeho spolubyvajuceho, mozu zapnut len svoje alebo spolocne

from flask import Flask, request, url_for, abort, jsonify
import requests
from json import loads
from datetime import datetime
import time

app = Flask("webserver")

lights_id = {"obyvakLight": 0, "koupelnaLight": 0, "kuchyneLight": 0, "karsobLight": 0, "karlikLight": 0,
           "karlosLight": 0, "juliaLight": 0}
switches_id = {"obyvakSwitch": 0, "koupelnaSwitch": 0, "kuchyneSwitch": 0, "karsobSwitch": 0, "karlikSwitch": 0,
           "karlosSwitch": 0, "juliaSwitch": 0}
motion_id = {"obyvakMotion": 0, "kuchyneMotion": 0}


for light in lights_id:
    print(light)
    get_response = requests.get("https://home_automation.iamroot.eu/newSmartLight")
    id = loads(get_response.text)["id"]
    lights_id.update({light: id})
"""
for switch in switches_id:
    print(switch)
    get_response = requests.get("https://home_automation.iamroot.eu/newSwitchSensor")
    id = loads(get_response.text)["id"]
    switches_id.update({switch: id})

for motion in motion_id:
    print(motion)
    get_response = requests.get("https://home_automation.iamroot.eu/newMotionSensor")
    id = loads(get_response.text)["id"]
    motion_id.update({motion: id})

"""

print(datetime.now().time())  # https://www.programiz.com/python-programming/datetime/current-time
sunset = 18
sunrise = 6
proportion_color = 4200
now_time = str(datetime.now().time())
now_time = int(now_time[:2])*60 + int(now_time[3:5])
print(now_time)
if now_time > sunset*60:  # 17:00
    time_before = now_time
    while now_time < sunset*60 + 90:  # 18:30
        now_time = str(datetime.now().time())
        now_time = int(now_time[:2]) * 60 + int(now_time[3:5])
        if time_before + 1 < now_time:
            time_before = now_time
            proportion_color -= 47 #235
            for light in lights_id:
                id = lights_id[light]
                time.sleep(0.2)
                print("idem poslat request")
                get_response = requests.get(f"https://home_automation.iamroot.eu/device/{id}/color_temperature/{2300+proportion_color}")
                print(loads(get_response.text))



    minutes = datetime.now().time()
    print(minutes)



for i in lights_id.items():
    print(i)
for i in switches_id.items():
    print(i)
for i in motion_id.items():
    print(i)


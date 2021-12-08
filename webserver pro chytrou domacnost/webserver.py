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
import flask
from flask import Flask, request, url_for, abort, jsonify, render_template, escape, redirect
import requests
from json import loads
from datetime import datetime
import time

app = Flask("webserver")
app.secret_key = "3FauQvwhSo4mpcc"
#app.config["TEMPLATES_AUTO_RELOAD"] = True
session = {}
lights_id = {"obyvakLight": 0, "koupelnaLight": 0, "kuchyneLight": 0, "karsobLight": 0, "karlikLight": 0,
             "karlosLight": 0, "juliaLight": 0}
light_status = {}
switches_id = {"obyvakSwitch": 0, "koupelnaSwitch": 0, "kuchyneSwitch": 0, "karsobSwitch": 0, "karlikSwitch": 0,
               "karlosSwitch": 0, "juliaSwitch": 0}
motion_id = {"obyvakMotion": 0, "kuchyneMotion": 0}

for light in lights_id:
    print(light)
    get_response = requests.get("https://home_automation.iamroot.eu/newSmartLight")
    id = loads(get_response.text)["id"]
    lights_id.update({light: id})
    light_status[lights_id[light]] = loads(get_response.text)["current_state"]
    print(light_status)
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


# zmena farby svetla podla casu
@app.route("/cron")
def change_color():
    print(datetime.now().time())  # https://www.programiz.com/python-programming/datetime/current-time
    sunset = 17
    sunrise = 6
    proportion_color = 4200
    now_time = str(datetime.now().time())
    now_time = int(now_time[:2]) * 60 + int(now_time[3:5])
    print(now_time)
    if sunset * 60 + 90 > now_time > sunset * 60:  # 17:00
        time_before = now_time
        while now_time < sunset * 60 + 90:  # 18:30
            now_time = str(datetime.now().time())
            now_time = int(now_time[:2]) * 60 + int(now_time[3:5])
            if time_before + 5 < now_time:
                time_before = now_time
                proportion_color -= 235
                for light in lights_id:
                    id = lights_id[light]
                    time.sleep(0.2)
                    print("idem poslat request")
                    get_response = requests.get(
                        f"https://home_automation.iamroot.eu/device/{id}/color_temperature/{2300 + proportion_color}")
                    print(loads(get_response.text))

    elif sunrise * 60 + 90 > now_time > sunrise * 60:  # 6:00
        time_before = now_time
        while now_time < sunrise * 60 + 90:  # 7:30
            now_time = str(datetime.now().time())
            now_time = int(now_time[:2]) * 60 + int(now_time[3:5])
            if time_before + 5 < now_time:
                time_before = now_time
                proportion_color += 235
                for light in lights_id:
                    id = lights_id[light]
                    time.sleep(0.2)
                    print("idem poslat request")
                    get_response = requests.get(
                        f"https://home_automation.iamroot.eu/device/{id}/color_temperature/{2300 + proportion_color}")
                    print(loads(get_response.text))


@app.route("/<device>/info")
def toggle_light(device):
    id = escape(device)
    print("som tu 1")
    get_response = requests.get(f"https://home_automation.iamroot.eu/device/{id}/toggle")
    light_status[id] = loads(get_response.text)["current_state"]
    print("som tu 2", get_response.text)
    return render_template("devices.html", lights_id=lights_id, light_status=light_status)
"""
@app.route("/update", methods=["GET"])
def get_status():
    light_status = light_status
    return jsonify(light_status=light_status)
"""

@app.route("/map")
def devices():
    if "username" not in session:
        return "You are not logged in <br><a href = '/'>" + "click here to log in</a>"
    username = session["username"]
    password = session["password"]
    print(username, password)
    lights_id = karsob["lights"]
    #return "Logged in as " + username + '<br>' + password + "<b><a href = '/logout'>click here to log out</a></b>"
    return render_template("devices.html", lights_id=lights_id, light_status=light_status, username=username)

karsob = {"lights": lights_id, "switches": switches_id}
karlos = {"lights": {"karlosLight": lights_id["karlosLight"], "kuchyneLight": lights_id["kuchyneLight"],
                     "obyvakLight": lights_id["obyvakLight"]},
          "switches": {"karlosSwitch": switches_id["karlosSwitch"], "kuchyneSwitch": switches_id["kuchyneSwitch"],
                       "obyvakSwitch": switches_id["obyvakSwitch"]}}
julia = {"lights": {"juliaLight": lights_id["juliaLight"], "kuchyneLight": lights_id["kuchyneLight"],
                    "obyvakLight": lights_id["obyvakLight"]},
         "switches": {"juliaSwitch": switches_id["juliaSwitch"], "kuchyneSwitch": switches_id["kuchyneSwitch"],
                      "obyvakSwitch": switches_id["obyvakSwitch"]}}
karlik = {"lights": {"karlikLight": lights_id["karlikLight"], "kuchyneLight": lights_id["kuchyneLight"],
                     "obyvakLight": lights_id["obyvakLight"]},
          "switches": {"karlikSwitch": switches_id["karlikSwitch"], "kuchyneSwitch": switches_id["kuchyneSwitch"],
                       "obyvakSwitch": switches_id["obyvakSwitch"]}}


def show_register_page() -> str:
    return f"""
    <form action="{url_for('register')}" method="post">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit">
    </form>
    """


def handle_register(register_form):
    print(register_form["username"], register_form["password"])
    username = register_form["username"]
    password = register_form["password"]
    userdata = (username, password)
    print("userdata", userdata)
    # https://pythonbasics.org/flask-sessions/
    # https://stackoverflow.com/questions/41865329/flask-session-and-multiple-users
    if userdata in [("karsob", "karsob"), ("karlos", "karlos"), ("julia", "julia"), ("karlik", "karlik")]:
        session["username"] = username
        session["password"] = password
        print(session)
        return redirect("/map")
    else:
        return f"""
        Invalid login 
        """


@app.route("/", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        return handle_register(request.form)
    else:
        if "username" in session:
            return redirect(url_for("devices"))
        else:
            return show_register_page()

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("password", None)
    return redirect(url_for("register"))

for i in lights_id.items():
    print(i)
for i in switches_id.items():
    print(i)
for i in motion_id.items():
    print(i)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    #app.run(debug=True, host='0.0.0.0')
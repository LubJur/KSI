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
            print(get_response.text)


@app.route("/<device>/info")
def toggle_light(device):
    id = escape(device)
    get_response = requests.get(f"https://home_automation.iamroot.eu/device/{id}/toggle")
    light_status[id] = loads(get_response.text)["current_state"]
    return render_template("devices.html", lights_id=lights_id, light_status=light_status)

@app.route("/update_status", methods=["POST"])
def update_status():
    print(light_status)
    print(light_status.get(lights_id[light]))
    return jsonify({"result": light_status.get(lights_id[light])})

"""
@app.route("/update", methods=["GET"])
def get_status():
    light_status = light_status
    return jsonify(light_status=light_status)
    
                var update = function(){
                    $.get(&#39;/23da16b1-7444-40a0-8a66-a833b7019408/info&#39;); 
                    $('#devices').load('/map' + ' #devices');
                });
            
"""

@app.route("/map")
def devices():
    print("som v devices")
    if "username" not in session:
        return "You are not logged in <br><a href = '/'>" + "click here to log in</a>"
    username = session["username"]
    password = session["password"]
    lights_id = karsob["lights"]
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
    # https://pythonbasics.org/flask-sessions/
    # https://stackoverflow.com/questions/41865329/flask-session-and-multiple-users
    if userdata in [("karsob", "karsob"), ("karlos", "karlos"), ("julia", "julia"), ("karlik", "karlik")]:
        session["username"] = username
        session["password"] = password
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
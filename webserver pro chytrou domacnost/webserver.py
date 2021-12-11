from flask import Flask, request, url_for, render_template, escape, redirect
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
switches_id = {"obyvakSwitch": 0, "koupelnaSwitch": 0, "kuchyneSwitch": 0, "karsobSwitch": 0, "karlikSwitch": 0,
               "karlosSwitch": 0, "juliaSwitch": 0}
motion_id = {"obyvakMotion": 0, "kuchyneMotion": 0}

for light in lights_id:
    print(light)
    get_response = requests.get("https://home_automation.iamroot.eu/newSmartLight")
    uuid = loads(get_response.text)["id"]
    lights_id.update({light: uuid})

for switch in switches_id:
    print(switch)
    get_response = requests.get("https://home_automation.iamroot.eu/newSwitchSensor")
    uuid = loads(get_response.text)["id"]
    switches_id.update({switch: uuid})
    light = switch[:-6]+"Light"
    print(lights_id[light])
    url_change = requests.get(f"http://home_automation.iamroot.eu/device/{uuid}/report_url?url="
                              f"http://home_automation.iamroot.eu/device/{lights_id[light]}/toggle")

for motion in motion_id:
    print(motion)
    get_response = requests.get("https://home_automation.iamroot.eu/newMotionSensor")
    uuid = loads(get_response.text)["id"]
    motion_id.update({motion: uuid})
    light = motion[:-6]+"Light"
    print(lights_id[light])
    url_change = requests.get(f"http://home_automation.iamroot.eu/device/{uuid}/report_url?url="
                              f"http://home_automation.iamroot.eu/device/{lights_id[light]}/state/on")

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
    # hours * 60 + minutes, so we only work in minutes
    now_time = int(now_time.strftime("%H")) * 60 + int(now_time.strftime("%M"))

    if sunset + 90 >= now_time >= sunset:  # when now_time is after sunset  6500 -> 2300
        change_needed = True
        # starting_color - ((now_time - sunset) * change_in_minute)
        color = 6500 - ((now_time - sunset) * (4200/90))

    elif sunrise >= now_time >= sunrise - 90:
        change_needed = True
        # (now_time - (sunrise - 90 min)) * change_in_minute + starting_color
        color = (now_time - (sunrise - 90)) * (4200/90) + 2300

    if change_needed:
        color = round(color)
        for light in lights_id:
            id = lights_id[light]
            time.sleep(0.2)
            get_response = requests.get(
                f"https://home_automation.iamroot.eu/device/{id}/color_temperature/{color}")
            print(get_response.text)


@app.route("/<device>/toggle")
def toggle_light(device):
    id = escape(device)
    print(id)
    get_response = requests.get(f"https://home_automation.iamroot.eu/device/{id}/toggle")
    print(get_response)
    return f"""
        Status changed on light with id {id}. <br>
        {loads(get_response.text)}
        """


@app.route("/<device>/info")
def device_info(device):
    id = escape(device)
    get_response = requests.get(f"https://home_automation.iamroot.eu/device/{id}")
    info = loads(get_response.text)
    actions = info["actions"]
    return render_template("device_info.html", info=info, actions=actions)


@app.route("/menu")
def junction():
    if "username" not in session:
        return "You are not logged in <br><a href = '/'>" + "click here to log in</a>"
    username = session["username"]
    return f"""
    Logged in as { username } <br>
    <a href = "/logout">Log out</a>
    <br>
    <a href = "/map"> Map </a> <br>
    <a href = "/controls"> Controls </a> <br>
    <a href = "/devices"> Devices </a> <br>
    <a href = "/heating"> Heating payment </a>
    """


@app.route("/map")
def map():
    if "username" not in session:
        return "You are not logged in <br><a href = '/'>" + "click here to log in</a>"
    username = session["username"]
    light_status = {}
    for light in lights_id:
        get_response = requests.get(f"https://home_automation.iamroot.eu/device/{lights_id[light]}")
        light_status[light] = [loads(get_response.text)["current_state"], loads(get_response.text)["color_temperature"]]
    return render_template("map.html", light_status=light_status, username=username)


@app.route("/controls")
def controls():
    if "username" not in session:
        return "You are not logged in <br><a href = '/'>" + "click here to log in</a>"
    username = session["username"]
    personal = ""
    obyvak = lights_id["obyvakLight"]
    kuchyne = lights_id["kuchyneLight"]
    if username == "karsob":
        personal = lights_id["karsobLight"]
    elif username == "karlos":
        personal = lights_id["karlosLight"]
    elif username == "julia":
        personal = lights_id["juliaLight"]
    elif username == "karlik":
        personal = lights_id["karlikLight"]
    return render_template("controls.html", personal=personal, obyvak=obyvak, kuchyne=kuchyne, username=username)


@app.route("/devices")
def devices():
    if "username" not in session:
        return "You are not logged in <br><a href = '/'>" + "click here to log in</a>"
    username = session["username"]
    return render_template("devices.html", lights_id=lights_id, motion_id=motion_id, switches_id=switches_id)

@app.route("/heating")
def heating():
    if "username" not in session:
        return "You are not logged in <br><a href = '/'>" + "click here to log in</a>"
    username = session["username"]
    karsob = requests.get(f"https://home_automation.iamroot.eu/device/{lights_id['karsobLight']}")
    karlos = requests.get(f"https://home_automation.iamroot.eu/device/{lights_id['karlosLight']}")
    julia = requests.get(f"https://home_automation.iamroot.eu/device/{lights_id['juliaLight']}")
    karlik = requests.get(f"https://home_automation.iamroot.eu/device/{lights_id['karlikLight']}")
    karsob = loads(karsob.text)["power_usage"]
    karlos = loads(karlos.text)["power_usage"]
    julia = loads(julia.text)["power_usage"]
    karlik = loads(karlik.text)["power_usage"]
    try:
        full = karsob + karlos + julia + karlik
        karsob = (karsob / full) * 100
        karlos = (karlos / full) * 100
        julia = (julia / full) * 100
        karlik = (karlik / full) * 100
        return render_template("heating.html", full=full, karsob=round(karsob, 2), karlos=round(karlos, 2),
                               julia=round(julia, 2), karlik=round(karlik, 2), username=username)
    except ZeroDivisionError:
        return "No one has used heating yet"


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
        return redirect("/menu")
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


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

from flask import Flask, request, url_for, render_template, escape, redirect
import requests
from json import loads
from datetime import datetime
import time
from suntime import Sun

app = Flask("webserver")
app.secret_key = "3z5FrwH6ABhOGpf13H7JPw"
session = {}

lights_id = {'obyvakLight': 'eae0a655-12d9-4cd0-a7c7-1001880bdd73',
             'koupelnaLight': '14c714ea-64f0-4cc5-b4aa-c9ce848cfeac',
             'kuchyneLight': '29a8de2c-4ed1-4253-bd1e-f4711a547a19',
             'karsobLight': '13d58f59-9cc6-4d19-aeca-9ec0a17709cd',
             'karlikLight': '29e5a9c3-d524-4ea8-9544-e27c6f2cf1e6',
             'karlosLight': '97febd6f-c437-46e8-a6a5-eff0752ba207',
             'juliaLight': '89a47532-edc5-415b-b3e9-825d7db411f8'}
switches_id = {'obyvakSwitch': '1b8ec9ae-918f-4e8e-a3d8-687b69ebcfad',
               'koupelnaSwitch': '92e0456f-296c-47d8-beec-2b105d8702ad',
               'kuchyneSwitch': '2a9bcb4e-b31d-467d-a752-2b525dc4e6ab',
               'karsobSwitch': '8fcb4b3c-9919-4690-82a0-1d546863f39e',
               'karlikSwitch': '886b075f-e3f0-49d1-a36a-9ed9ccce5496',
               'karlosSwitch': '12d42109-1e41-4095-84c3-a18dcae85fb7',
               'juliaSwitch': '9e4ab651-ba30-4261-a6c1-aa1bf1513eb2'}
motion_id = {'obyvakMotion': '759f3d8a-d515-4e2a-80d6-60d516470fb7',
             'kuchyneMotion': 'ba5ce109-150f-4d04-9948-b93e27334f8b'}

"""
# For creating new lights, switches, motion sensors
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
"""


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
    if "username" not in session:
        return "You are not logged in <br><a href = '/'>" + "click here to log in</a>"
    id = escape(device)
    get_response = requests.get(f"https://home_automation.iamroot.eu/device/{id}")
    info = loads(get_response.text)
    actions = info["actions"]
    username = session["username"]
    type = info["type"]
    safe = False
    # https://stackoverflow.com/questions/8023306/get-key-by-value-in-dictionary
    if type == "SmartLight":
        if list(lights_id.keys())[list(lights_id.values()).index(id)] in [(username+"Light"), "kuchyneLight",
                                                                          "obyvakLight"]:
            safe = True
    elif type == "SwitchSensor":
        if list(switches_id.keys())[list(switches_id.values()).index(id)] in [(username+"Switch"), "kuchyneSwitch",
                                                                              "obyvakSwitch"]:
            safe = True
    print(safe)
    return render_template("device_info.html", info=info, actions=actions, username=username, safe=safe)


@app.route("/<device>/info_safe")
def device_info_safe(device):
    id = escape(device)
    get_response = requests.get(f"https://home_automation.iamroot.eu/device/{id}")
    info = loads(get_response.text)
    actions = info["actions"]
    username = session["username"]
    return render_template("device_info.html", info=info, actions=actions, username=username)

@app.route("/menu")
def junction():
    if "username" not in session:
        return "You are not logged in <br><a href = '/'>" + "click here to log in</a>"
    username = session["username"]
    return f"""
    <style></style>
    Logged in as { username } <br>
    <a href = "/logout">Log out</a>
    <h2>Menu</h2>
    <button><a href = "/map"> Map </a></button> <br>
    <button><a href = "/controls"> Controls </a></button> <br>
    <button><a href = "/devices"> Devices </a></button> <br>
    <button><a href = "/heating"> Heating payment </a></button>
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
    return render_template("devices.html", lights_id=lights_id, motion_id=motion_id, switches_id=switches_id,
                           username=username)


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
    This site uses cookies.
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

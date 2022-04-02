import requests  # python -m pip install -U requests

#print(requests.post("https://losoviny.iamroot.eu/part_one_login", data={"username": "Loskarlos",
#                                                                  "password": "JednohoDneOvladnuKSI"}))

from time import sleep

data = {
    'username': 'Loskarlos',
    'password': 'JednohoDneOvladnuKSI',
}

#session = requests.Session()
#print(session.options("https://losoviny.iamroot.eu/part_two").text)
post_response = requests.post('https://losoviny.iamroot.eu/part_two_login', data=data)
print(post_response)
#print(post_response.json())
print(post_response.cookies)

#header = post_response.json()["auth_token"]
#header = {"Authorization": "Bearer " + header}
#print(header)

get_response = requests.get("https://losoviny.iamroot.eu/part_two", cookies=post_response.cookies)
print(get_response)
print(get_response.text)  # {"flag":"NevERgONnALEtYOuDown","msg":"OK"}
sleep(2)

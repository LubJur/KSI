import requests

session = requests.Session()
#escapepath = "../../"
#userpass = "foo"
filepath = "/kreslenie a dialogy/upload.png"

#data = {"name": escapepath, "password": userpass}

#print(session.post("http://127.0.0.1:5000/login", data=data))
session.cookies.set("user_id", "9752408304", domain="127.0.0.1:5000")
print(session.cookies)
# 9752408304
files = {"file": ("foo.png", open(filepath, "rb"), "text/plain")}
print(session.post("http://127.0.0.1:5000/new_submission", files=files))

"""
session.cookies.set("user_id", "2187796908", domain="127.0.0.1:5000")
#print(session.get("http://127.0.0.1:5000/submission/test"))

file = open("/home/lubomir/Desktop/Gymnázium/4. ročník/KSI/kreslenie a dialogy/upload.png", "rb")
print(session.post("http://127.0.0.1:5000/new_submission", data=file))
file.close()
"""
import socket, pynetstring, base64
import tkinter
from tkinter import Tk, ttk, StringVar, IntVar
import tkinter.filedialog

window = Tk()

decoder = pynetstring.Decoder()
"""
hostname = "159.89.4.84"
port = 42069
name = "LubJur"
password = "silne_heslo"
description = "nieco"
isNSFW = "false"
meme = base64.b64encode(open("/home/lubomir/Pictures/drog.png", "rb").read()).decode("ascii")
token = ""
data_port = 0
data_token = ""
data_sum = 0
status = ""
"""

hostname = tkinter.StringVar()
port = tkinter.StringVar()
name = tkinter.StringVar()
password = tkinter.StringVar()
description = tkinter.StringVar()
isNSFW = tkinter.StringVar()
meme = ""
status = StringVar()

hostname.set("159.89.4.84")
port.set(42069)
name.set("LubJur")
#password.set("silne_heslo")
description.set("nieco")
isNSFW.set("false")
meme = base64.b64encode(open("E:\Lubomir Jurcisin\Obrázky\w1mt5k97uxq11.jpg", "rb").read()).decode("ascii")

status.set("Waiting to send meme")


def check_data(hostname, port, name, password, description, isNSFW, meme):
    print(type(port))
    print(port)
    print(port > 65535 or port < 0)
    if type(port) != int or (port > 65535 or port < 0):
        status_txt.config(text="ERROR: Port must be a number from 0 to 65535")
        window.update_idletasks()
        return
    else:
        connect(hostname, port, name, password, description, isNSFW, meme)


def connect(hostname, port, name, password, description, isNSFW, meme):
    token = ""
    data_port = 0
    data_token = ""
    data_sum = 0
    global status
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((hostname, port))
        s.sendall(pynetstring.encode("C MTP V:1.0"))
        data = s.recv(1024)
        s.sendall(pynetstring.encode(f"C {name}"))
        token = s.recv(1024)
        token = token.decode()[5:-1]
        data_port = s.recv(1024)
        data_port = data_port.decode()[4:-1]
        status_txt.config(text="Connecting to data channel")
        window.update_idletasks()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d:
            d.connect((hostname, int(data_port)))
            d.sendall(pynetstring.encode(f"C {name}"))
            data_sum = 0
            data_sum_temp = 0
            len_sent = 0
            status_txt.config(text="Authenticating")
            window.update_idletasks()
            if d.recv(1024).decode()[5:-1] != token:
                status_txt.config(text="ERROR: Tokens do not match")
                window.update_idletasks()
                return

            while True:
                request = decoder.feed(d.recv(1024))
                request = request[0].decode()[2:]
                print("request:", request)

                if request[:4] == "ACK:":
                    data_sum_temp = int(request[4:])
                    print(len_sent, data_sum_temp)
                    if data_sum_temp == len_sent:
                        data_sum += data_sum_temp
                        print("v poriadku")
                    else:
                        print("error")
                    print(data_sum_temp)

                elif request == "REQ:meme":
                    status_txt.config(text="Sending meme...")  # this takes the longest time so it has a status msg
                    window.update_idletasks()
                    d.sendall(pynetstring.encode(f"C {meme}"))
                    #data_sum_temp = decoder.feed(d.recv(1024))
                    #data_sum_temp = int(data_sum_temp[0].decode()[6:])
                    len_sent = len(meme)
                    """
                    if data_sum_temp != len(meme):
                        status_txt.config(text="ERROR: Bytes do not match")
                        window.update_idletasks()
                        return
                    else:
                        data_sum = data_sum + data_sum_temp
                        status_txt.config(text="Meme sent")
                        window.update_idletasks()
                        status = "Memes sent"
                        print("data sum:", data_sum)
                    """
                elif request == "REQ:description":
                    d.sendall(pynetstring.encode(f"C {description}"))
                    #data_sum_temp = decoder.feed(d.recv(1024))
                    #data_sum_temp = int(data_sum_temp[0].decode()[6:])
                    len_sent = len(description)
                    """
                    if data_sum_temp != len(description):
                        status_txt.config(text="ERROR: Bytes do not match")
                        window.update_idletasks()
                        return
                    else:
                        data_sum = data_sum + data_sum_temp
                        status_txt.config(text="Description sent")
                        window.update_idletasks()
                        print("data sum:", data_sum)
                    """
                elif request == "REQ:isNSFW":
                    d.sendall(pynetstring.encode(f"C {isNSFW}"))
                    #data_sum_temp = decoder.feed(d.recv(1024))
                    print(data_sum_temp)
                    len_sent = len(isNSFW)
                    #data_sum_temp = int(data_sum_temp[0].decode()[6:])
                    """
                    if data_sum_temp != len(isNSFW):
                        status_txt.config(text="ERROR: Bytes do not match")
                        window.update_idletasks()
                        return
                    else:
                        data_sum = data_sum + data_sum_temp
                        status_txt.config(text="NSFW flag sent")
                        window.update_idletasks()
                        print("data sum:", data_sum)
                    """
                elif request == "REQ:password":
                    d.sendall(pynetstring.encode(f"C {password}"))
                    #data_sum_temp = decoder.feed(d.recv(1024))
                    #data_sum_temp = int(data_sum_temp[0].decode()[6:])
                    len_sent = len(password)
                    """
                    if data_sum_temp != len(password):
                        status_txt.config(text="ERROR: Bytes do not match")
                        window.update_idletasks()
                        return
                    else:
                        data_sum = data_sum + data_sum_temp
                        status_txt.config(text="Password sent")
                        window.update_idletasks()
                        print("data sum:", data_sum)
                    """
                elif request[0:3] == "END":
                    status_txt.config(text="Finishing sending")
                    window.update_idletasks()
                    data_token = request
                    data_token = data_token[4:]
                    print("data_token:", data_token)
                    break

                else:
                    print(request[1:])
                    status_txt.config(text=f"ERROR: {request[1:]}")
                    window.update_idletasks()
                    print("nastala chyba pri posielani dat")
                    return

        msglen = decoder.feed(s.recv(1024))
        msglen = msglen[0].decode()[2:]
        print("sucet_dat", msglen)
        if int(msglen) != data_sum:
            status_txt.config(text="ERROR: Not all data sent")
            window.update_idletasks()
            print("Neboli poslane vsetky dáta")
            return
        s.sendall(pynetstring.encode(f"C {data_token}"))
        success = decoder.feed(s.recv(1024))
        success = success[0].decode()[2:]
        if success == "ACK":
            status_txt.config(text="SUCCESS")
            window.update_idletasks()
            status = "Successfully sent meme"
            print("SUCCESS")



def browseFiles():
    filename = tkinter.filedialog.askopenfilename(filetypes=[("jpeg files", "*.jpg"), ("png files", "*.png")])
    global meme
    meme = base64.b64encode(open(filename, "rb").read()).decode("ascii")
    print(filename)


ip_label = ttk.Label(window, text="IP address:")
ip_label.grid(row=1, column=1)

ip_entry = ttk.Entry(window, textvariable=hostname)
ip_entry.grid(row=1, column=2)

port_label = ttk.Label(window, text="Port:")
port_label.grid(row=1, column=3)

port_entry = ttk.Entry(window, textvariable=port)
port_entry.grid(row=1, column=4)

nick_label = ttk.Label(window, text="nick:")
nick_label.grid(row=2, column=1)

nick_entry = ttk.Entry(window, textvariable=name)
nick_entry.grid(row=2, column=2)

password_label = ttk.Label(window, text="password:")
password_label.grid(row=2, column=3)

password_entry = ttk.Entry(window, textvariable=password)
password_entry.grid(row=2, column=4)

nsfw_check = ttk.Checkbutton(window, text="NSFW", variable=isNSFW)
nsfw_check.grid(row=3, column=1)

description_label = ttk.Label(window, text="Description:")
description_label.grid(row=4, column=1)

description_entry = ttk.Entry(window, textvariable=description)
description_entry.grid(row=4, column=2, rowspan=1, columnspan=3, ipadx=50)

browse_btn = ttk.Button(window, text="Browse", command=browseFiles)
browse_btn.grid(row=5, column=1)

status_txt = ttk.Label(window, text="status")
status_txt.grid(row=5, column=2, columnspan=2)

send_btn = ttk.Button(window, text="Send", command=lambda: connect(hostname.get(), int(port.get()), name.get(), password.get(), description.get(), isNSFW.get(), meme))
send_btn.grid(row=5, column=4)

window.mainloop()

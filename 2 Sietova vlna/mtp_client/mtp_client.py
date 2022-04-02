import socket, pynetstring, base64
import tkinter
from tkinter import Tk, ttk, StringVar, filedialog
from PIL import ImageTk, Image

window = Tk()
window.resizable(False, False)
window.title("MTP client")

decoder = pynetstring.Decoder()


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
name.set("")
password.set("")
description.set("")
isNSFW.set("false")
filename = ""


def check_data(hostname, port, name, password, description, isNSFW, meme):
    if description == "":
        # server is expecting data in format C <data>, we cant pass nothing even though string is empty
        description = " "

    if type(port) != int or (port > 65535 or port < 0):
        status.set("ERROR: Port must be a number from 0 to 65535")
        window.update_idletasks()
        return
    elif hostname == "":
        status.set("ERROR: Hostname must not be empty")
        window.update_idletasks()
        return
    elif name == "":
        status.set("ERROR: Nick must not be empty")
        window.update_idletasks()
        return
    elif password == "":
        status.set("ERROR: Password must not be empty")
        window.update_idletasks()
        return
    elif meme == "":
        status.set("ERROR: You must choose a meme")
        window.update_idletasks()
        return
    else:
        send_btn["state"] = "disabled"
        connect(hostname, port, name, password, description, isNSFW, meme)


def connect(hostname, port, name, password, description, isNSFW, meme):
    global status, status_txt
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        status.set("Connecting...")
        window.update()  # https://stackoverflow.com/questions/24167053/tkinter-label-doesnt-update
        s.connect((hostname, port))
        s.sendall(pynetstring.encode("C MTP V:1.0"))
        data = decoder.feed(s.recv(1024))
        if data[0].decode() != "S MTP V:1.0":
            s.sendall(pynetstring.encode("E server is not responding"))
            status.set("E Server is not responding")
            window.update()
            send_btn["state"] = "enable"
            return
        s.sendall(pynetstring.encode(f"C {name}"))

        token = decoder.feed(s.recv(1024))
        token = token[0].decode()
        if token == "":
            s.sendall(pynetstring.encode("E token not received"))
            status.set("E token not received")
            window.update()
            send_btn["state"] = "enable"
            return
        data_port = decoder.feed(s.recv(1024))
        data_port = data_port[0].decode()
        if data_port[0] == "E":
            s.sendall(pynetstring.encode("E data port not received"))
            status.set("E data port not received")
            window.update()
            send_btn["state"] = "enable"
            return
        data_port = data_port[2:]
        status.set("Sending data...")
        window.update()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as d:
            d.connect((hostname, int(data_port)))
            d.sendall(pynetstring.encode(f"C {name}"))
            data_sum = 0
            len_sent = 0
            if decoder.feed(d.recv(1024))[0].decode() != token:
                s.sendall(pynetstring.encode("E tokens do not match"))
                status.set("E tokens do not match")
                window.update()
                send_btn["state"] = "enable"
                return

            while True:
                request = decoder.feed(d.recv(1024))
                request = request[0].decode()[2:]
                print("request:", request)

                if request[:4] == "ACK:":
                    data_sum_temp = int(request[4:])
                    if data_sum_temp == len_sent:
                        data_sum += data_sum_temp
                    else:
                        status.set("ERROR: not all data sent")
                        window.update()
                        send_btn["state"] = "enable"
                        return

                elif request == "REQ:meme":
                    status.set("Sending meme...")
                    d.sendall(pynetstring.encode(f"C {meme}"))
                    len_sent = len(meme)

                elif request == "REQ:description":
                    status.set("Sending description...")
                    d.sendall(pynetstring.encode(f"C {description}"))
                    len_sent = len(description)

                elif request == "REQ:isNSFW":
                    status.set("Sending NSFW tag...")
                    d.sendall(pynetstring.encode(f"C {isNSFW}"))
                    len_sent = len(isNSFW)

                elif request == "REQ:password":
                    status.set("Sending password...")
                    d.sendall(pynetstring.encode(f"C {password}"))
                    len_sent = len(password)

                elif request[0:3] == "END":
                    data_token = request[4:]
                    print("data_token:", data_token)
                    break

                else:
                    s.sendall(pynetstring.encode(f"E {request}"))
                    status.set(f"E {request}")
                    window.update()
                    send_btn["state"] = "enable"
                    return
                window.update()

        msglen = decoder.feed(s.recv(1024))
        msglen = msglen[0].decode()[2:]
        print("data_sent:", msglen)
        if int(msglen) != data_sum:
            s.sendall(pynetstring.encode("E not all data sent"))
            status.set("E Not all data sent")
            window.update()
            send_btn["state"] = "enable"
            return
        s.sendall(pynetstring.encode(f"C {data_token}"))
        success = decoder.feed(s.recv(1024))
        success = success[0].decode()[2:]
        if success == "ACK":
            status.set("SUCCESS")
            window.update()
            print("SUCCESS")
            send_btn["state"] = "enable"
        else:
            s.sendall(pynetstring.encode("E ACK message not received"))
            status.set("E ACK message not received")
            window.update()
            send_btn["state"] = "enable"


def browseFiles():
    # https://stackoverflow.com/questions/10133856/how-to-add-an-image-in-tkinter
    global meme, filename
    filename = tkinter.filedialog.askopenfilename(filetypes=[("jpeg files", "*.jpg"), ("png files", "*.png")])
    if filename != "":
        meme = base64.b64encode(open(filename, "rb").read()).decode("ascii")
        filename = ImageTk.PhotoImage(Image.open(filename).resize((400, 400)))
        preview = ttk.Label(window, image=filename)
        preview.grid(row=6, column=1, columnspan=4)
    else:
        filename = ""
        meme = ""


ip_label = ttk.Label(window, text="IP address:")
ip_label.grid(row=1, column=1)

ip_entry = ttk.Entry(window, textvariable=hostname)
ip_entry.grid(row=1, column=2)

port_label = ttk.Label(window, text="Port:")
port_label.grid(row=1, column=3)

port_entry = ttk.Entry(window, textvariable=port)
port_entry.grid(row=1, column=4)

nick_label = ttk.Label(window, text="Nick:")
nick_label.grid(row=2, column=1)

nick_entry = ttk.Entry(window, textvariable=name)
nick_entry.grid(row=2, column=2)

password_label = ttk.Label(window, text="Password:")
password_label.grid(row=2, column=3)

password_entry = ttk.Entry(window, textvariable=password)
password_entry.grid(row=2, column=4)

nsfw_check = ttk.Checkbutton(window, text="NSFW", variable=isNSFW, onvalue="true", offvalue="false")
nsfw_check.grid(row=3, column=1)

description_label = ttk.Label(window, text="Description:")
description_label.grid(row=4, column=1)

description_entry = ttk.Entry(window, textvariable=description)
description_entry.grid(row=4, column=2, rowspan=1, columnspan=3, sticky="ew")

browse_btn = ttk.Button(window, text="Browse", command=browseFiles)
browse_btn.grid(row=5, column=1)

status_txt = ttk.Label(window, textvariable=status)
status_txt.grid(row=5, column=2, columnspan=3, sticky="w")

send_btn = ttk.Button(window, text="Send",
                      command=lambda: check_data(hostname.get(), int(port.get()), name.get(), password.get(),
                                                 description.get(), isNSFW.get(), meme))
send_btn.grid(row=5, column=4, sticky="ew")

window.mainloop()

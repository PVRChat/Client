import socket
import threading
import json
import os

print()
print("  ______     ______   ____ _           _      ____ _ _            _   ")
print(" |  _ \ \   / /  _ \ / ___| |__   __ _| |_   / ___| (_) ___ _ __ | |_ ")
print(" | |_) \ \ / /| |_) | |   | '_ \ / _` | __| | |   | | |/ _ \ '_ \| __|")
print(" |  __/ \ V / |  _ <| |___| | | | (_| | |_  | |___| | |  __/ | | | |_ ")
print(" |_|     \_/  |_| \_\\\\____|_| |_|\__,_|\__|  \____|_|_|\___|_| |_|\__|")
print("                                                                      ")
print()

print("Set server IP")
IP = input()
print("Set the server port or press ENTER for default")
port = input()
if port != "":
    port = int(port)
    PORT = port
else:
    PORT = 4007

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

if not os.path.exists("username.conf"):
    with open("username.conf", 'w') as conf_file:
        nick = input("Entrer your username : ")
        data = {
            "name": nick
            }
        json.dump(data, conf_file)
    with open("username.conf", 'r') as conf_file:
        conf = json.load(conf_file)
else:
    with open("username.conf", 'r') as conf_file:
        conf = json.load(conf_file)

nick = conf["name"]
client_socket.send(nick.encode())

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print()
                print(message)
        except:
            print("An error occurred.")
            client_socket.close()
            break

def send():
    while True:
        message = input("New message < ")
        full_message = f"{message}"
        client_socket.send(full_message.encode())

receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()

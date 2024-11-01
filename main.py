from data.var import *
import sqlite3
import hashlib
import getpass
import socket
import threading


class main:
    def __init__(self):
        self.conn = sqlite3.connect(dataBaseFile)
        self.cursor = self.conn.cursor()
        self.cursor.executescript(dbInit)
        self.conn.commit()
        self.conn.close()
        self.main()

    def main(self):
        while True:
            print("-" * 70)
            print("1. Connect")
            print("2. Register")
            print("3. Add server")
            print("4. Delete server")
            print("5. Exit")
            choice = input("Choice < ")
            if choice == "1":
                self.connect(input("Server name < "))
            elif choice == "2":
                self.register()
            elif choice == "3":
                self.addServer()
            elif choice == "4":
                self.deleteServer()
            elif choice == "5":
                break
            else:
                print("Invalid choice")
        pass

    def login(self):
        self.conn = sqlite3.connect(dataBaseFile)
        self.cursor = self.conn.cursor()
        username = input("Username < ")
        password = hashlib.sha256(getpass.getpass("Password < ").encode()).hexdigest()
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = self.cursor.fetchone()
        if user:
            print("Login successful")
            return user
        else:
            print("Login failed")
            return False
        self.conn.close()
        pass
    def register(self):
        self.conn = sqlite3.connect(dataBaseFile)
        self.cursor = self.conn.cursor()
        username = input("Username < ")
        password = hashlib.sha256(getpass.getpass("Password < ").encode()).hexdigest()
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()
        self.conn.close()
        print("User created")
        pass
    def addServer(self):
        self.conn = sqlite3.connect(dataBaseFile)
        self.cursor = self.conn.cursor()

        while True:
            name = input("Server name < ")
            ip = input("Server IP < ")
            port = input("Server port < ")

            if name == "" or ip == "":
                print("Cannot add server")
                print("Server name and IP are required")
                return
            if port == "":
                port = 4007
                print("Port set to default 4007")
                break
            else:
                port = int(port)
                break

        if self.cursor.execute("SELECT * FROM servers WHERE name = ? AND ip = ? AND port = ?", (name, ip, port)).fetchone():
            print("Server already exists")
            return

        self.cursor.execute("INSERT INTO servers (name, ip, port) VALUES (?, ?, ?)", (name, ip, port))
        self.conn.commit()
        self.conn.close()
        pass
    def deleteServer(self):
        self.conn = sqlite3.connect(dataBaseFile)
        self.cursor = self.conn.cursor()
        name = input("Server name < ")

        if not self.cursor.execute("SELECT * FROM servers WHERE name = ?", (name,)).fetchone():
            print("Server not found")
            return

        self.cursor.execute("DELETE FROM servers WHERE name = ?", (name,))
        print("Server deleted")

        self.conn.commit()
        self.conn.close()
        pass
    def connect(self, serverName):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.conn = sqlite3.connect(dataBaseFile)
        self.cursor = self.conn.cursor()

        server = self.cursor.execute("SELECT * FROM servers WHERE name = ?", (serverName,)).fetchone()
        if not server:
            print("Server not found")
            return
        ip = server[2]
        port = int(server[3])

        user = self.login()
        if not user:
            return

        username = user[1]

        client_socket.connect((ip, port))
        client_socket.send(username.encode())

        def receive():
            while True:
                try:
                    message = client_socket.recv(1024).decode()
                    if message:
                        print()
                        print(message)
                        print("<")
                except Exception as e:
                    print("An error occurred.")
                    print(e)
                    client_socket.close()
                    break
        def send():
            while True:
                try:
                    message = input("New message < ")
                    if message == "exit":
                        client_socket.close()
                        break
                    full_message = f"{message}"
                    client_socket.send(full_message.encode())
                except Exception as e:
                    print(e)
                    client_socket.close()
                    break

        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        send_thread = threading.Thread(target=send)
        send_thread.start()

        receive_thread.join()
        send_thread.join()

        pass

if __name__ == "__main__":
    print(motd)
    main()
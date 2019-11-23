# Code from freeCodeCamp.org at https://www.youtube.com/watch?v=McoDjOCb2Zo
import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = input("Enter server IP: ")
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print("Your entity ID is:", self.id)

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, data):
        try:
            # print("Sent:", data)
            self.client.send(str.encode(data))
            result = self.client.recv(2048).decode("utf-8")
            # if data == "spr":
            #     print("Entity count:", result)
            # print("Received:", result)
            # print("--------------")
            return result
        except socket.error as e:
            print(e)

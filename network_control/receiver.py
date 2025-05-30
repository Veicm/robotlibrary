import socket
import _thread
from robotlibrary.network_control.connector import Connector

class CommandReceiver:
    def __init__(self, ssid, password, port=1234):
        self.connector = Connector(ssid, password)
        self.port = port
        self.running = False
        self.handlers = {}
    
    def define(self, command:str, handler):
        '''Save a handler for a certain command.'''
        self.handlers[command] = handler

    def start(self):
        """Start receiving on a different thread"""
        self.connector.connect_to_wifi()
        self.running = True
        _thread.start_new_thread(self._listen, ())

    def stop(self):
        self.running = False

    def _listen(self):
        addr = socket.getaddrinfo('0.0.0.0', self.port)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)

        print(f"CommandReceiver is running on port {self.port}")

        while self.running:
            #try:
            client, addr = s.accept()
            data = client.recv(1024).decode().strip()
            print("Received:", data)

            if data in self.handlers:
                self.handlers[data]("_")  # execute callback
            else:
                print("Unknown command:", data)

            client.close()
            #except Exception as e:
            #print("Error while listing:", e)

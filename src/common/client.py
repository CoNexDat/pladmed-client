#!/usr/bin/env python

import urllib.request
import urllib.parse
import json
import subprocess

class Client:
    def __init__(self):
        pass
    
    def connect(self):
        print("Client connected")

        try:
            response = urllib.request.urlopen('http://0.0.0.0:5000/')
            print(json.loads(response.read()))
        except:
            print("Can't reach server")

        subprocess.run(["dig", "www.google.com"])
        #result = subprocess.run(["scamper", "-c", "trace -P UDP-paris", "-i", "179.60.195.36"])

    def disconnect(self):
        print("Client disconnected")

    def on_message(self, data):
        print("Received: ", data)

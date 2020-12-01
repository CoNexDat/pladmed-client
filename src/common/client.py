#!/usr/bin/env python

import urllib.request
import urllib.parse
import json
import subprocess
from utils.params_parser import ParamsParser

class Client:
    def __init__(self):
        self.parser = ParamsParser()
    
    def connect(self):
        print("Client connected")

        '''try:
            response = urllib.request.urlopen('http://0.0.0.0:5000/')
            print(json.loads(response.read()))
        except:
            print("Can't reach server")

        subprocess.run(["dig", "www.google.com"])'''
        #result = subprocess.run(["scamper", "-c", "trace -P UDP-paris", "-i", "179.60.195.36"])

    def traceroute(self, params):
        # Params must be a dict with params
        sub_cmd = self.parser.parse_traceroute(params)

        result = subprocess.run(
            ["scamper", "-c"] + sub_cmd
        )

    def disconnect(self):
        print("Client disconnected")

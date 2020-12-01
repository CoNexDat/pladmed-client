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

        result = self.execute_scamper(sub_cmd)

        print(f"Operation finished with result {result}")

    def ping(self, params):
        # Params must be a dict with params
        sub_cmd = self.parser.parse_ping(params)
        result = self.execute_scamper(sub_cmd)

        print(f"Operation finished with result {result}")

    def execute_scamper(self, sub_cmd):
        print("Executing scamper -c with params: ", sub_cmd)

        return subprocess.run(
            ["scamper", "-c"] + sub_cmd
        )

        print(f"Operation finished with result {result}")

    def dns(self, params):
        sub_cmd = self.parser.parse_dns(params)

        print("Executing dig with params: ", sub_cmd)

        result = subprocess.run(
            ["dig"] + sub_cmd
        )

        print(f"Operation finished with result {result}")

    def disconnect(self):
        print("Client disconnected")

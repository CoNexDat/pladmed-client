#!/usr/bin/env python

import urllib.request
import urllib.parse
import json
import subprocess
from utils.params_parser import ParamsParser
from crontab import CronTab

class Client:
    def __init__(self, storage):
        self.parser = ParamsParser()
        self.storage = storage
    
    def connect(self):
        print("Client connected")

    def traceroute(self, op_id, params):
        # Params must be a dict with params
        sub_cmd = self.parser.parse_traceroute(params)

        result = self.execute_scamper(op_id, sub_cmd)

        print(f"Operation finished with result {result}")

    def ping(self, op_id, params):
        # Params must be a dict with params
        with CronTab(user=True) as cron:
            job = cron.new(command='echo "hola" >> /file.txt')
            job.setall('* * * * *')
        sub_cmd = self.parser.parse_ping(params)
        result = self.execute_scamper(op_id, sub_cmd)

        print(f"Operation finished with result {result}")

    def execute_scamper(self, op_id, sub_cmd):
        print("Executing scamper -c with params: ", sub_cmd)

        return subprocess.run(
            [
                "scamper",
                "-O",
                "warts",
                "-o",
                self.storage.create_operation_filename(op_id),
                "-c"
            ] + sub_cmd
        )

    def disconnect(self):
        print("Client disconnected")

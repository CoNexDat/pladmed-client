#!/usr/bin/env python

import urllib.request
import urllib.parse
import json
import subprocess
from crontab import CronTab
from utils.params_parser import ParamsParser

class Client:
    def __init__(self, storage):
        self.parser = ParamsParser()
        self.storage = storage
    
    def connect(self):
        print("Client connected")

    def traceroute(self, op_id, params):
        # Params must be a dict with params
        sub_cmd = self.parser.parse_traceroute(params)
        self.execute_scamper(op_id, sub_cmd, params["cron"], params["times_per_minute"], params["stop_time"])

    def ping(self, op_id, params):
        # Params must be a dict with params
        sub_cmd = self.parser.parse_ping(params)
        self.execute_scamper(op_id, sub_cmd, params["cron"], params["times_per_minute"], params["stop_time"])

    def execute_scamper(self, op_id, sub_cmd, cron_expression, times_per_minute, stop_time):
        print("Executing scamper -c with params: ", sub_cmd)
        # filename = self.storage.create_operation_filename(op_id)
        sub_cmd_str = " ".join([f"'{param}'" for param in sub_cmd])
        cron_command = f"python3 /src/scripts/scamper.py {op_id} {times_per_minute} {sub_cmd_str}"
        print(cron_command)
        # Saves execution cron
        with CronTab(user=True) as cron:
            job = cron.new(command=cron_command, comment=op_id)
            job.setall(cron_expression)
        # Saves stopping cron
        with CronTab(user=True) as cron:
            stop_command = f"python3 /src/scripts/stopper.py {op_id}"
            job = cron.new(command=stop_command, comment=op_id)
            job.setall(stop_time)

    def disconnect(self):
        print("Client disconnected")

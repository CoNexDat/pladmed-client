#!/usr/bin/env python

import urllib.request
import urllib.parse
import json
import subprocess
from utils.params_parser import ParamsParser
from common.transmit_manager import TransmitManager
import time

class Client:
    def __init__(self, sio, storage, operations_manager):
        self.sio = sio
        self.parser = ParamsParser()
        self.storage = storage
        self.operations_manager = operations_manager
        self.transmit_manager = TransmitManager(self.sio, self.operations_manager)

    def connect(self):
        print("Client connected")

        # Notify pending operations to transmit manager
        self.operations_manager.start()
        self.transmit_manager.start()

    def disconnect(self):
        print("Client disconnected")

        self.transmit_manager.stop()
        self.operations_manager.stop()

    def traceroute(self, op_id, params):
        # Params must be a dict with params
        sub_cmd = self.parser.parse_traceroute(params)

        result = self.execute_scamper(op_id, sub_cmd)

    def ping(self, op_id, params):
        # Params must be a dict with params
        sub_cmd = self.parser.parse_ping(params)
        result = self.execute_scamper(op_id, sub_cmd)

    def execute_scamper(self, op_id, sub_cmd):
        print("Executing scamper -c with params: ", sub_cmd)

        self.operations_manager.add_operation(op_id)

        subprocess.run(
            [
                "scamper",
                "-O",
                "warts",
                "-o",
                self.storage.create_operation_filename(op_id),
                "-c"
            ] + sub_cmd
        )

        self.operations_manager.end_operation(op_id)
        self.transmit_manager.notify_end_operation(op_id)

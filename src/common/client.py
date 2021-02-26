#!/usr/bin/env python

import urllib.request
import urllib.parse
import subprocess
from utils.params_parser import ParamsParser
from common.transmit_manager import TransmitManager
from common.operations_manager import OperationsManager
from common.operation import Operation
from common.communicator import Communicator
import time

class Client:
    def __init__(self, sio, storage, max_credits):
        self.sio = sio
        self.parser = ParamsParser()
        self.storage = storage
        
        self.communicator = Communicator()

        self.operations_manager = OperationsManager(storage, self.communicator)

        self.transmit_manager = TransmitManager(
            self.sio,
            storage,
            self.communicator
        )

        print("Client with availability for up to: ", max_credits, " creditos")

        self.max_credits = max_credits

        self.operations_manager.start()

    def connect(self):
        print("Client connected")
        self.transmit_manager.start()

    def disconnect(self):
        print("Client disconnected")

        self.transmit_manager.stop()

    def traceroute(self, op_id, params, credits_):
        # Params must be a dict with params
        actual_credits = self.communicator.get_current_credits()

        print("Credits in use: ", actual_credits, "/", self.max_credits)

        sub_cmd = self.parser.parse_traceroute(params)

        operation = Operation(op_id, sub_cmd, credits_)

        self.operations_manager.add_operation(operation)

    def ping(self, op_id, params, credits_):
        # Params must be a dict with params
        sub_cmd = self.parser.parse_ping(params)

        operation = Operation(op_id, sub_cmd, credits_)

        self.operations_manager.add_operation(operation)

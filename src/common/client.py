#!/usr/bin/env python

import urllib.request
import urllib.parse
import subprocess
from utils.params_parser import ParamsParser
from common.transmit_manager import TransmitManager
from common.operations_manager import OperationsManager
from common.operation import Operation
import time

class Client:
    def __init__(self, sio, storage, operations_manager):
        self.sio = sio
        self.parser = ParamsParser()
        self.storage = storage
        self.operations_manager = operations_manager  
        self.transmit_manager = TransmitManager(
            self.sio,
            self.storage,
            self.operations_manager
        )

        self.execute_pending_tasks()
    
    def execute_pending_tasks(self):
        finished_ops = self.operations_manager.finished_operations()
        in_process_ops = self.operations_manager.in_process_operations()

        # Notify pending operations to transmit manager
        for operation in finished_ops:
            self.transmit_manager.notify_end_operation(operation)

        # Execute pending operations
        for operation in in_process_ops:
            self.execute_scamper(operation)

    def connect(self):
        print("Client connected")
        self.operations_manager.start()
        self.transmit_manager.start()

    def disconnect(self):
        print("Client disconnected")

        self.transmit_manager.stop()
        self.operations_manager.stop()

    def traceroute(self, op_id, params):
        # Params must be a dict with params
        sub_cmd = self.parser.parse_traceroute(params)

        operation = Operation(op_id, sub_cmd)

        result = self.execute_scamper(operation)

    def ping(self, op_id, params):
        # Params must be a dict with params
        sub_cmd = self.parser.parse_ping(params)

        operation = Operation(op_id, sub_cmd)

        result = self.execute_scamper(operation)

    def execute_scamper(self, operation):
        print("Executing scamper -c with params: ", operation.params)

        self.operations_manager.add_operation(operation)

        subprocess.run(
            [
                "scamper",
                "-O",
                "warts",
                "-o",
                self.storage.operation_filename_tmp(operation),
                "-c"
            ] + operation.params
        )

        self.operations_manager.end_operation(operation)
        self.transmit_manager.notify_end_operation(operation)

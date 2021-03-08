#!/usr/bin/env python

import urllib.request
import urllib.parse
import subprocess
from utils.params_parser import ParamsParser
from common.transmit_manager import TransmitManager
from common.operations_manager import OperationsManager
from common.finish_task_communicator import FinishTaskCommunicator
from common.finish_operation_communicator import FinishOperationCommunicator
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

        self.finish_task_communicator = FinishTaskCommunicator(self.communicator)
        self.finish_operation_communicator = FinishOperationCommunicator(self.communicator)

        self.transmit_manager = TransmitManager(
            self.sio,
            storage,
            self.communicator
        )

        print("Client with availability for up to: ", max_credits, " creditos")

        self.max_credits = max_credits

        self.operations_manager.start()
        self.finish_task_communicator.start()
        self.finish_operation_communicator.start()

    def start_connection(self, host):
        actual_credits = self.communicator.get_current_credits()

        self.sio.connect(
            url=host,
            transports='websocket',
            headers={
                "total_credits": str(self.max_credits),
                "in_use_credits": str(actual_credits)
            }
        )

    def connect(self):
        print("Client connected")
        self.transmit_manager.start()
        #self.finish_task_communicator.start()
        #self.finish_operation_communicator.start()

    def disconnect(self):
        print("Client disconnected")

        self.transmit_manager.stop()
        #self.finish_task_communicator.stop()
        #self.finish_operation_communicator.stop()

    def traceroute(self, op_id, params, credits_):
        # Params must be a dict with params
        actual_credits = self.communicator.get_current_credits()

        print("Credit cost: ", credits_)
        print("Credits in use: ", actual_credits, "/", self.max_credits)

        if actual_credits + credits_ > self.max_credits:
            print("No available credits for this operation")
            return
            
        sub_cmd = self.parser.parse_traceroute(params)

        print("Sub cmd: ", sub_cmd)

        operation = Operation(
            op_id,
            sub_cmd,
            credits_,
            params["cron"],
            params["times_per_minute"],
            params["stop_time"]
        )

        self.operations_manager.add_operation(operation)

    def ping(self, op_id, params, credits_):
        # Params must be a dict with params
        actual_credits = self.communicator.get_current_credits()

        print("Credit cost: ", credits_)
        print("Credits in use: ", actual_credits, "/", self.max_credits)

        if actual_credits + credits_ > self.max_credits:
            print("No available credits for this operation")
            return

        sub_cmd = self.parser.parse_ping(params)

        operation = Operation(
            op_id,
            sub_cmd,
            credits_,
            params["cron"],
            params["times_per_minute"],
            params["stop_time"]
        )

        self.operations_manager.add_operation(operation)

    def delete(self, op_id, params, credits_):
        print(f"Deleting operation ${op_id}")
        operation = Operation(
            op_id,
            None,
            credits_,
            params["cron"],
            params["times_per_minute"],
            params["stop_time"]
        )
        self.operations_manager.cancel_operation(operation)

#!/usr/bin/env python

import urllib.request
import urllib.parse
import subprocess
from crontab import CronTab
from utils.params_parser import ParamsParser
from common.transmit_manager import TransmitManager
from common.operations_manager import OperationsManager
from common.operation import Operation
from utils.time_utils import is_over

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

        operation = Operation(op_id, sub_cmd, params["cron"], params["times_per_minute"], params["stop_time"])
        self.execute_scamper(operation)

    def ping(self, op_id, params):
        # Params must be a dict with params
        sub_cmd = self.parser.parse_ping(params)

        operation = Operation(op_id, sub_cmd, params["cron"], params["times_per_minute"], params["stop_time"])
        self.execute_scamper(operation)

    def execute_scamper(self, operation):
        print("Executing scamper -c with params: ", operation.params)
        if is_over(operation.stop_time):
            # What should I do here?
            self.operations_manager.end_operation(operation)
            # self.transmit_manager.notify_end_operation(operation)
        sub_cmd_str = " ".join([f"'{param}'" for param in operation.params])
        cron_command = f"python3 /src/scripts/scamper.py {operation.id} {operation.times_per_minute} {sub_cmd_str}"
        # Saves execution cron
        with CronTab(user=True) as cron:
            job = cron.new(command=cron_command, comment=operation.id)
            job.setall(operation.cron_expression)
        # Saves stopping cron
        with CronTab(user=True) as cron:
            stop_command = f"python3 /src/scripts/stopper.py {operation.id}"
            job = cron.new(command=stop_command, comment=operation.id)
            job.setall(operation.stop_time)

        # TODO: Mover esto al scamper.py de alguna forma
        # self.operations_manager.end_operation(operation)
        # Esto se puede pasar el delete_operation?
        self.transmit_manager.notify_end_operation(operation)

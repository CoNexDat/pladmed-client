import sys
import os

sys.path.append(os.path.abspath(os.path.join('../..', 'src')))

import subprocess
import sys
import time
import uuid
import json
from multiprocessing.connection import Client
from common.task import Task
from os import path, getenv
import config.connection as config

address = ('localhost', int(getenv('FINISH_TASK_PORT')))

#TMP_FOLDER = "../safe_storage/tmp/"

def operation_filename(task):
    file_storage = config.TMP_FOLDER + task.code

    return file_storage 

def end_task(operation_str, task, client):
    print(f'Sending to FinishTaskCommunicator operation {operation_str}')

    finished_task_data = {
        "operation": json.loads(operation_str),
        "task": task.data()
    }

    client.send(json.dumps(finished_task_data))

def main():
    print(sys.argv)
    print("Scamper main called")

    client = Client(address)

    times_per_minute = int(sys.argv[1])

    print(f"times_per_minute: {times_per_minute}")

    sub_cmd_joined = sys.argv[2]
    
    print(f"sub_cmd_joined: {sub_cmd_joined}")

    sub_cmd = sub_cmd_joined.split("|")

    print("Sub cmd splitted: ", sub_cmd)

    operation_str = sys.argv[3]

    print(f"operation_str: {operation_str}")

    for i in range(times_per_minute):
        start = time.time()
        task = Task(str(uuid.uuid4()))

        subprocess.run(
            [
                "scamper",
                "-O",
                "warts",
                "-o",
                operation_filename(task),
                "-c"
            ] + sub_cmd
        )

        time.sleep(max(60/times_per_minute - int(time.time() - start), 0))
        end_task(operation_str, task, client)

    client.close()

if __name__ == "__main__":
    print("Scamper called")
    main()

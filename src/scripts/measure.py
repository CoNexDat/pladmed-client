import os
import sys
import subprocess
import time
import uuid
import json

sys.path.append(os.path.abspath(os.path.join('../..', 'src')))

from multiprocessing.connection import Client
from common.operation import SCAMPER_BINARY, DIG_BINARY
from common.task import Task
from os import path, getenv
import config.connection as config

address = ('localhost', int(getenv('FINISH_TASK_PORT')))

#TMP_FOLDER = "../safe_storage/tmp/"


def operation_filename(task):
    file_storage = config.TMP_FOLDER + task.code

    return file_storage


def end_task(operation_str, task, client):
    finished_task_data = {
        "operation": json.loads(operation_str),
        "task": task.data()
    }

    client.send(json.dumps(finished_task_data))


def main():
    times_per_minute = int(sys.argv[1])

    # This is a really quick fix. You should not create more than 1 client
    for i in range(times_per_minute):
        client = Client(address)

        sub_cmd_joined = sys.argv[2]

        sub_cmd = sub_cmd_joined.split("|")

        operation_str = sys.argv[3]

        binary = sys.argv[4]

        run_measurement = run_scamper if binary == SCAMPER_BINARY else run_dig
    
        start = time.time()
        task = Task(str(uuid.uuid4()))

        run_measurement(task, sub_cmd)

        time.sleep(max(60 / times_per_minute - int(time.time() - start), 0))
        
        end_task(operation_str, task, client)

        client.close()


def run_scamper(task, sub_cmd):
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


def run_dig(task, sub_cmd):
    dig_cmd = 'dig ' + ' '.join(sub_cmd)
    with open(operation_filename(task), "w") as outfile:
        subprocess.run(
            f"{dig_cmd} | gzip",
            shell=True,
            stdout=outfile
        )


if __name__ == "__main__":
    main()

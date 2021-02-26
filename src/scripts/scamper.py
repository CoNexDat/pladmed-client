import subprocess
import sys
import time
from multiprocessing.connection import Listener
from os import path, getenv

address = ('localhost', 0)

NEW_DATA = 1

IN_PROCESS = 0
FINISHED = 1


def create_operation_filename(op_id):
    store_in = "/src/results/"
    file_storage = store_in + op_id

    i = 1
    while path.exists(file_storage):
        file_storage = store_in + op_id + "_part_" + str(i)
        i += 1

    return file_storage


def add_operation(operation, listener):
    listener.send(NEW_DATA)
    listener.send([operation, IN_PROCESS])


def end_operation(operation, listener):
    listener.send(NEW_DATA)
    listener.send([operation, FINISHED])


def main():
    print(sys.argv)
    listener = Listener(address, authkey=b'secret password')
    op_id = sys.argv[1]
    print(f"op_id: {op_id}")
    cron = sys.argv[2]
    print(f"cron: {cron}")
    times_per_minute = int(sys.argv[3])
    print(f"times_per_minute: {times_per_minute}")
    stop_time = sys.argv[4]
    print(f"stop_time: {stop_time}")
    sub_cmd = sys.argv[5:]
    print(f"sub_cmd: {stop_time}")
    operation = {
        "id": op_id,
        "cron": cron,
        "times_per_minute": times_per_minute,
        "stop_time": stop_time,
        "params": sub_cmd
    }
    add_operation(operation, listener.accept())
    for i in range(times_per_minute):
        start = time.time()
        filename = create_operation_filename(op_id)
        subprocess.run(
            [
                "scamper",
                "-O",
                "warts",
                "-o",
                filename,
                "-c"
            ] + sub_cmd
        )
        time.sleep(max(60/times_per_minute - int(time.time() - start), 0))
    end_operation(operation)


if __name__ == "__main__":
    main()

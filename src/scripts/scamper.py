import subprocess
import sys
import time
import uuid
from multiprocessing.connection import Listener
from os import path, getenv

address = ('localhost', int(getenv('FINISH_TASK_PORT')))

TMP_FOLDER = "../safe_storage/tmp/"


def create_operation_filename(task_code):
    file_storage = TMP_FOLDER + task_code

    i = 1
    while path.exists(file_storage):
        file_storage = TMP_FOLDER + task_code + "_part_" + str(i)
        i += 1

    return file_storage


def end_task(operation_str, listener):
    print(f'Sending to FinishTaskCommunicator operation {operation_str}')
    listener.send(operation_str)


def main():
    print(sys.argv)
    listener = Listener(address, authkey=b'secret password')
    conn = listener.accept()
    times_per_minute = int(sys.argv[1])
    print(f"times_per_minute: {times_per_minute}")
    sub_cmd_joined = sys.argv[2]
    print(f"sub_cmd_joined: {sub_cmd_joined}")
    sub_cmd = sub_cmd_joined.split()
    operation_str = sys.argv[3]
    print(f"operation_str: {operation_str}")
    for i in range(times_per_minute):
        start = time.time()
        task_code = str(uuid.uuid4())
        filename = create_operation_filename(task_code)
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
        end_task(operation_str, conn)
    conn.close()


if __name__ == "__main__":
    main()
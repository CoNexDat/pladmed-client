import subprocess
import sys
import time
from os import path
# from common.storage import Storage
# import config.connection as config


def create_operation_filename(op_id):
    store_in = "/src/results/"
    file_storage = store_in + op_id

    i = 1
    while path.exists(file_storage):
        file_storage = store_in + op_id + "_part_" + str(i)
        i += 1

    return file_storage


def main():
    print(sys.argv)
    op_id = sys.argv[1]
    times_per_minute = int(sys.argv[2])
    sub_cmd = sys.argv[3:]
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


if __name__ == "__main__":
    main()

import subprocess
import sys
from os import path
# from common.storage import Storage
# import config.connection as config


def create_operation_filename(op_id):
    store_in = "results/"
    file_storage = store_in + op_id

    i = 1
    while path.exists(file_storage):
        file_storage = op_id + "_part_" + str(i)
        i += 1

    return file_storage


def main():
    print(sys.argv)
    op_id = sys.argv[1]
    sub_cmd = sys.argv[2:]
    filename = create_operation_filename(op_id)
    print(subprocess.run(
        [
            "scamper",
            "-O",
            "warts",
            "-o",
            filename,
            "-c"
        ] + sub_cmd
    ))


if __name__ == "__main__":
    main()

import sys
from os import path, getenv
from crontab import CronTab
from multiprocessing.connection import Listener

address = ('localhost', int(getenv('FINISH_OPERATION_PORT')))


def end_operation(operation_str, listener):
    print(f'Sending to FinishOperationCommunicator operation {operation_str}')
    listener.send(operation_str)


def main():
    print(sys.argv)
    listener = Listener(address, authkey=b'secret password')
    conn = listener.accept()
    op_id = sys.argv[1]
    print(f"op_id: {op_id}")
    operation_str = sys.argv[2]
    print(f"operation_str: {operation_str}")
    with CronTab(user=True) as cron:
        job_iter = cron.find_comment(op_id)
        for job in job_iter:
            cron.remove(job)
    end_operation(operation_str, conn)
    conn.close()


if __name__ == "__main__":
    main()
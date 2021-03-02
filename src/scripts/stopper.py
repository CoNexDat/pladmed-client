import sys
import os

sys.path.append(os.path.abspath(os.path.join('../..', 'src')))

from os import path, getenv
from crontab import CronTab
from multiprocessing.connection import Client

address = ('localhost', int(getenv('FINISH_OPERATION_PORT')))

def end_operation(operation_str, client):
    print(f'Sending to FinishOperationCommunicator operation {operation_str}')
    client.send(operation_str)

def main():
    print(sys.argv)
    client = Client(address)

    op_id = sys.argv[1]

    print(f"op_id: {op_id}")

    operation_str = sys.argv[2]

    print(f"operation_str: {operation_str}")

    print("Removing a CRON")

    with CronTab(user=True) as cron:
        job_iter = cron.find_comment(op_id)

        for job in job_iter:
            print("Removing job...")
            cron.remove(job)

    end_operation(operation_str, client)
    client.close()

if __name__ == "__main__":
    print("Stopper called")
    main()
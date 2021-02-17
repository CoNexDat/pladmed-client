import sys
from crontab import CronTab


def main():
    print(sys.argv)
    op_id = sys.argv[1]
    with CronTab(user=True) as cron:
        job_iter = cron.find_comment(op_id)
        for job in job_iter:
            cron.remove(job)


if __name__ == "__main__":
    main()
from croniter import croniter
from datetime import datetime, timedelta

def is_over(operation):
    date = datetime.strptime(operation.stop_time, '%d/%m/%Y %H:%M')
    today = datetime.today()

    diff_time = date - today

    return diff_time.days < 0

def generate_stoptime(operation):
    date = datetime.strptime(operation.stop_time, '%d/%m/%Y %H:%M')

    return (
        str(date.minute) + " " +
        str(date.hour) + " " +
        str(date.day) + " " +
        str(date.month) + " *"
    )

#!/usr/bin/env python3

from multiprocessing.connection import Listener, Client
from socket import AF_INET, SOCK_DGRAM
import datetime
import sys
import socket
import struct
import subprocess
import time
import os

CLOSE_MESSAGE = "close"
SYNC_MESSAGE = "sync"
SYNC_PASSWORD = b'sync password'


def listen():
    port = int(os.getenv('TIME_SYNC_PORT'))
    address = ('localhost', port)  # family is deduced to be 'AF_INET'
    listener = Listener(address, authkey=SYNC_PASSWORD)
    while True:
        print(f'Listening for time sync connections on port {port}...')
        conn = listener.accept()
        print(f'Time sync connection accepted from {listener.last_accepted}')
        msg = conn.recv()
        if msg == SYNC_MESSAGE:
            print('Received sync message')
            sync()
            conn.close()


def sync():
    ntp_server_url = os.getenv('NTP_SERVER', 'ntp_server')
    print(f"Will sync with ntp server at {ntp_server_url}")
    try:
        ntp_time = getNTPTime(ntp_server_url)
        print(f"Time obtained from server: {ntp_time}")
        # Set time in container (does not affect host)
        os.environ['FAKETIME'] = ntp_time_to_fake_time(ntp_time)
    except socket.timeout:
        print(f"Timed out waiting for NTP time from {ntp_server_url}")


def getNTPTime(host="pool.ntp.org"):
    port = 123
    buf = 1024
    address = (host, port)
    msg = '\x1b' + 47 * '\0'

    # reference time (in seconds since 1900-01-01 00:00:00)
    TIME1970 = 2208988800  # 1970-01-01 00:00:00

    # connect to server
    client = socket.socket(AF_INET, SOCK_DGRAM)
    client.sendto(msg.encode('utf-8'), address)

    client.settimeout(5)
    msg, address = client.recvfrom(buf)

    t = struct.unpack("!12I", msg)[10]
    t -= TIME1970
    return time.ctime(t).replace("  ", " ")


def ntp_time_to_fake_time(ntp_time):
    ntp_date = datetime.datetime.strptime(ntp_time, '%a %b %d %H:%M:%S %Y')
    return ntp_date.strftime("@%Y-%m-%d %H:%M:%S")

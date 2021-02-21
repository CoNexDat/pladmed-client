#!/usr/bin/env python3

from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct
import time
import os


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
    msg, address = client.recvfrom(buf)

    t = struct.unpack("!12I", msg)[10]
    t -= TIME1970
    return time.ctime(t).replace("  ", " ")


ntp_server_url = os.getenv('NTP_SERVER', 'ntp_server')
print(f"Will sync with ntp server at {ntp_server_url}")
ntp_time = getNTPTime(ntp_server_url)
print(f"Time obtained from server: {ntp_time}")

import os
import re
import sys
import socket
import struct

ip_pattern = re.compile("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")

def findIPAddress(value):
    try:
        # Might be a simple integer
        return int(value)
    except ValueError:
        m = ip_pattern.search(value)
        if m: # IP address in octet notation
	        return IPfromString(m.group())
        else: # Potentially a hostname
            return socket.gethostbyname(value)

def IPfromString(ip):
    return struct.unpack("!I", socket.inet_aton(ip))[0]

def IPtoString(ip):
    return socket.inet_ntoa(struct.pack("!I", int(ip)))

def MACfromString(mac):
    return int(mac.replace(':', ''), 16)

def MACtoString(mac):
    mac = hex(int(mac)).lstrip('0x')
    mac = '0'*(12-len(mac))+mac
    return ':'.join([mac[i:i+2] for i in range(0, len(mac), 2)])

def mask(ip, mask):
    mask = (1 << 32) - (1 << 32 >> mask)
    return int(ip) & mask

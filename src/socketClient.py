#!/usr/bin/env python

"""
A simple echo client
"""

import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:

    # Send data
    message = 'This is the message.  It will be repeated.'
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()


# import socket
#
# host = 'localhost'
# port = 49999
# size = 1024
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((host,port))
# dataToSend = bytearray([200,90])
# s.send(dataToSend)
# data = s.recv(size)
# for byte in data:
#     print 'Received:', hex(int(byte))
# s.close()

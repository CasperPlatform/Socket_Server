#!/usr/bin/env python
#from __future__ import print_function

"""
basic socket server
"""

import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                print >>sys.stderr, 'sending data back to the client'
                connection.sendall(data)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break

    finally:
        # Clean up the connection
        connection.close()

# import socket
#
# host = ''
# port = 49999
# backlog = 5
# size = 1024
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((host,port))
# s.listen(backlog)
# print ('server listening on port: ' + repr(port))
# while 1:
#     client, adress = s.accept()
#     data = client.recv(size)
#     if data:
#         print("received: "+repr(data))
#         client.send(data)
#     client.close()

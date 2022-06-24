#!/usr/bin/env python3
import TCPstreams5 as TCP
import struct
import random

IP = input("Host: ")
PORT = int(input("Port: "))

while True:
    CON = TCP.clientCon(IP,PORT)

    Query = input("Query: ")
    CON.senddat(struct.pack('!L',random.randint(1,1000)) + struct.pack('!L',0) + struct.pack('!L',1000) + struct.pack('!L',len(Query)) + Query.encode())
    print(CON.getdat())
    CON.close()

#!/usr/bin/env python3
import Searcher
import ConfigUtils
import Logger
import TCPstreams5 as TCP

import threading
import struct
import json

def upstreamRequest(host,ID,Iter,MaxDepth,QLength,Data):
    SP = host.split(':')
    CON = TCP.clientCon(SP[0],int(SP[1]))
    CON.senddat(
        struct.pack('!L',ID) + struct.pack('!L',Iter+1) + struct.pack('!L',MaxDepth) + struct.pack('!L',QLength) + Data
    )
    ResultCount = struct.unpack('!L',CON.getdat(4))[0]
    print("Result Count is",ResultCount)
    
    if (ResultCount != 0):
        Data = b''
        for i in range(ResultCount):
            D = CON.getdat(4)
            ResultLength = struct.unpack('!L',D)[0]
            Data += D
            Data += CON.getdat(ResultLength)
    else:
        Data = b''

    CON.close()

    return struct.pack('!L',ResultCount) + Data


#Packet Structure:
#Bytes, Each number refers to characters
#
# [4 * ID] [4 * Recursions] [4 * Recursion Depth] [4 * Length] Question
Previous = []
def clientHandle(CON,MYID,CONF,log,ser):
    global Previous

    ID = struct.unpack('!L',CON.getdat(4))[0]
    Iter = struct.unpack('!L',CON.getdat(4))[0]
    MaxDepth = struct.unpack('!L',CON.getdat(4))[0]
    QLength = struct.unpack('!L',CON.getdat(4))[0]
    DATA = CON.getdat(QLength)

    
   # print(Previous,ID)

    #Check if We have already got this message
    if ID in Previous:
        log.log(str(MYID) + " Query From Me")
        CON.senddat(struct.pack('!L',0))
        CON.close()
        return

    Previous = Previous[1:]
    Previous.append(ID)

    #If Max Depth, Expire
    if Iter > MaxDepth:
        log.log(str(MYID) + " Query Depth Exceeded")
        CON.senddat(struct.pack('!L',0))
        CON.close()
        return

    else:
        #Try Local Query
        results = ser.search(DATA)

        if len(results) == 0:
            log.log(str(MYID) + " Upstream query")
            for host in CONF['Upstream']:
                result = upstreamRequest(host,ID,Iter,MaxDepth,QLength,DATA)
                if len(result) != 4:
                    CON.senddat(result)

            CON.senddat(struct.pack('!L',0))

        else:
            log.log(str(MYID) + " Found")
            OUT = struct.pack('!L',len(results))
            for i in results:
                D = json.dumps(i).encode()
                OUT += struct.pack('!L',len(D))
                OUT += D
            print("Returning",OUT)
            CON.senddat(OUT)


    CON.close()



 

def main(ConfigPath):
    global Previous
    Config = ConfigUtils.complexParseConfig(ConfigPath)
    if type(Config['Upstream']) != list:
        Config['Upstream'] = [Config['Upstream']]
    log = Logger.logger(Config['Logfile'])
    log.log("Loaded Config")
    
    for i in range(int(Config['Tracker'])):
        Previous.append(0)

    Server = TCP.newServer(Config['HostIP'],int(Config['HostPort']))
    log.log("TCP Server Open")

    Search = Searcher.searcher(Config)

    Connections = []
    ID = 0
    while True:
        con = TCP.serverCon(Server)
        log.log("Accepted Client " + str(ID))
        t = threading.Thread(target=clientHandle,args=(con,ID,Config,log,Search))
        t.start()
        Connections.append({'Con':con,'Thread':t})
        ID += 1



if __name__ == '__main__':
    import sys
    main(sys.argv[1])

#Author: Yost
#Team BPWY

from socket import *
import json
#client calls into server to establish connection
def serverConnect(IPaddress):
    s=socket(AF_INET,SOCK_DGRAM)
    s.sendto('hello server'.encode(),('{}'.format(IPaddress),5000))
    portinfo=s.recvfrom(1024)
    port = int(portinfo[0])
    s=socket()
    s.connect((IPaddress,port))
    return s
	
#client receives info from server and then replies
def recvSend(data,s):
    jsonmessage=s.recv(1024)
    s.send(data.encode())
    print(jsonmessage)
    print(jsonmessage.decode())
    message = json.loads(jsonmessage.decode())
    return message
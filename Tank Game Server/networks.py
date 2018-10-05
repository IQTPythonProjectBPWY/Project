#Author: Yost
#Team BPWY

from socket import *
import json
#setup lists for sockets, clients, responses

def setupClients(numPlayers):
    sockets=[]  #for setupClients(numPlayers)
    clients=[]  #for setupClients(numPlayers)
    s0=socket(AF_INET,SOCK_DGRAM)
    s0.bind(('',5000))
    print('The server IP is {}'.format(gethostbyname(gethostname())))
    for x in range(1,numPlayers+1):
        port = 5000+x
        print('listening for player requests on port 5000')
        ts=socket()  #temporary socket
        sockets.append(ts)  #add to sockets[]
        tc ,ta = s0.recvfrom(1024) #what does client have to say?
        while tc != 'hello server'.encode():  #if client has correct password
            tc ,ta = s0.recvfrom(1024) 
        print ('player request recieved sending reconnection port - {}'.format(port))
        s0.sendto('{}'.format((port)).encode(),ta)  #tells client which port they can use
        sockets[x-1].bind(('',port))  #player 1 gets port 5001, etc.
        sockets[x-1].listen(1)  #looks for client on established port
        print('waiting for player to connect on port{}'.format(port))
        c,a = sockets[x-1].accept()
        print('player {} connected on port {}'.format(x,port))
        clients.append(c)  #add to clients[]
    return clients

def sendRecv(data,clients):
    responses=[]
    print(' preparing packet ')
    jsondata = json.dumps(data)
    for client in clients:
        client.send(jsondata.encode())
        stuff=client.recv(1024)
        responses.append(stuff.decode())  #store responses in responses[x-1]
    return responses
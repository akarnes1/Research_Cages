import socket
import sys
import csv
from thread import *
 
HOST = ''
PORT = 8888

currentRevs = [1,1,1,1,1,1,1,1]
dispenseRevs = [3,3,10,10,10,10,10,10]
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
s.listen(10)
print 'Socket now listening'
 

def clientthread(conn):
    conn.send('Connected')
    reply = "1"
     
    while True:  
        data = conn.recv(128)
        client = data.split(',')
        print str(client)
        index = int(client[1])
        if client[0] == "disp":
            reply = str(dispenseRevs[index])
            conn.sendall(reply)
            print reply
        elif client[0] == "current":
            reply = str(currentRevs[index])
            conn.sendall(reply)
            print reply
        elif client[0] == "save":
            dispenseRevs[index] = int(client[2])
        elif client[0] == "update":
            currentRevs[index] = int(client[2])
            
        if not data: 
            break
        
    conn.close()
 

while 1:
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    start_new_thread(clientthread ,(conn,))
 
s.close()

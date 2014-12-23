#!usr/bin/env python
#-*- coding:utf-8 -*-
# Server.py
import socket
import select
import sys
import random

def broadcast ( sock , msg ) :
    for sock in CONNECTION_LIST:
        if sock != server and socket != sock:
            try:
                sock.send(msg)
            except:
                sock.close()
                #sys.exit()
                CONNECTION_LIST.remove(sock)
                #total-=1

if __name__ == "__main__":

    line = raw_input("How many Players?")
    maxnum = int(line)
    
    
    HOST = ""
    PORT = 8889
    CONNECTION_LIST = []
    DICT = {}
    server = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
    server.setsockopt( socket.SOL_SOCKET , socket.SO_REUSEADDR , 1 )
    server.bind( (HOST,PORT) )
    server.listen(10)
    num = flag = 0
    CONNECTION_LIST.append(server)
    while 1:
        rd_sockets,wr_sockets,er_sockets = select.select(CONNECTION_LIST,[],[])
        for sock in rd_sockets:
            if sock == server:
                sockfd , addr = server.accept()
                CONNECTION_LIST.append(sockfd)
                DICT[sockfd] = num
                print(sockfd,num)
                if flag==0:
                    sockfd.send(str(num))
                num += 1
                if num == maxnum and flag==0:
                    flag = 1
                    broadcast(server,str(num))
            else:
                try:
                    data = sock.recv(4096)
                    if data[0]=='@':
                        x = random.randint(0,63)
                        y = random.randint(0,47)
                        msg = "@"+str(x)+","+str(y)
                        broadcast(sock,msg)
                    elif data:
                        broadcast(sock,data)
                except:
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    #total-=1
                    continue
                    #sys.exit()
    server.close()

#!/usr/bin/env python3
import socket, time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def handle_echo(addr, conn):
  print("Connected by", addr)

  full_data = conn.recv(BUFFER_SIZE) #receive data
  time.sleep(0.5) #wait a bit
  conn.sendall(full_data) #send it back
  conn.close() #close connection

def main():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    s.bind((HOST, PORT)) #bind socket to address
    s.listen(2) #set to listening mode
    
    #continuously listen for connections
    while True:
      conn, addr = s.accept()

      #start a process daemon for handling multiple connections
      p = Process(target = handle_echo, args = (addr, conn))
      p.daemon = True
      p.start()
      print("Started process ", p)

if __name__ == "__main__":
  main()
#!/usr/bin/env python3
import socket, time, sys

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def get_remote_ip(host):
  print(f'Getting IP from {host}')

  try:
    remote_ip = socket.gethostbyname(host)
  except socket.gaierror:
    print('Hostname could not be resolved. Exiting')
    sys.exit()
  
  print(f"IP address of {host} is {remote_ip}")

  return remote_ip

def main():
  extern_host = "www.google.com"
  port = 80

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
    # start proxy server
    print("Starting Proxy Server")

    proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_start.bind((HOST, PORT)) # bind socket to address
    proxy_start.listen(1) # set to listening mode

    while True:
      conn, addr = proxy_start.accept()
      print("Connected by" , addr)

      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
        # Connect to google
        print("Connecting to Google")
        remote_ip = get_remote_ip(extern_host)
        proxy_end.connect((remote_ip, port))
        
        #get data
        send_full_data = conn.recv(BUFFER_SIZE)

        #send data
        print(f"Sending received data {send_full_data} to google")
        proxy_end.sendall(send_full_data)

        proxy_end.shutdown(socket.SHUT_WR)

        data = proxy_end.recv(BUFFER_SIZE)
        print(f"Sending received data {data} to client")

        conn.send(data)
      
      conn.close() # close connection

if __name__ == "__main__":
  main()
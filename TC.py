from datetime import datetime
import socket
import threading
import numpy as np
import time
from _thread import *

node = ''
hostIP = '127.0.0.1'

portNumber = 1234

process = [1234, 2134, 2144]

clients_dt = []

transaction = {}
server_socket = None

X_Net = np.array([[0.09948112195726, 0.15, 0.33245127376045, 3.4360911798419]])
X_Net = np.array([[0.091604370148729, 0.10924611843482, 0.29356097449987, 3.4721042168745]])


def tc_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    try:
        while True:
            message = input("Enter your message (or 'exit' to quit): ")
            if message.lower() == "exit":
                break
            client_socket.sendall(message.encode())
            response = client_socket.recv(1024)
            print(f"Response from server: {response.decode()}")
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing connection.")
        client_socket.close()
        

def tc_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"TC Server listening on {host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"New connection from {client_address}")
            handle_client(client_socket)
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server_socket.close()

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            # Process the received data or implement TC logic here.
            # You can inspect the data to decide how to control traffic.
            # For simplicity, let's just echo the received data back to the client.
            client_socket.sendall(data)
    except:
        pass
    finally:
        print("Closing connection.")
        client_socket.close()
    
def thread_client(connection, address):
    global server_socket
    global clients_dt  
    global transaction
    connection.send(str.encode('prepare'))
    data = connection.recv(2048).decode('utf=8')
    print('received from ' + address[0] + ':' + str(address[1]) + ' ' + data)
    transaction[address[1]] = data
    if data == 'yes':
        print(address[0] + ':' + str(address[1]), ' Node sent Yes')
        
    print('sending commit to - ' + str(address[1]))
    connection.send(str.encode('commit'))
    transaction[address[1]] = 'commit'
    clients_dt.append('commit')
        
    connection.close()
    

def start_server(sender_port):
    global server_socket
    global clients_dt
    threads = []
    server_socket = socket.socket()
    try:
        server_socket.bind((hostIP, sender_port))
    except socket.error as e:
        print('Exception while creating sender', str(e))

    server_socket.listen(2)
    while (True):
        client, address = server_socket.accept()
        print(address[0] + ':' + str(address[1]) + ' is connected')
        t = threading.Thread(target = thread_client,args =(client, address, ))
        t.start()
        threads.append(t)
        
        if len(threads) >= 2:
            break
        
    for t in threads:
        t.join()
    
    time.sleep(20)
        
    server_socket.close()

if __name__ == "__main__":
    print("TC")
    sendProcess = 1
    sendport = process[sendProcess - 1]
    threading.Thread(target=start_server, args=(sendport,)).start()
    
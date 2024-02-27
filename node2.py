from datetime import datetime
import socket
import threading
import time

node = ''
hostIP = '127.0.0.1'

portNumber = 1234

process = [1234, 2134, 2144]

clients = []
transaction = []
server_socket = None
data = ''


Process_Client = [((0.13481688704114, 0.14256922246944, 0.75, 3.3163861235653), "Node1"),
        ((0.13075893272027, 0.14664056393281, 0.40788855987898, 2.9000019878594), "Node2"),
        ((0.093951164405388, 0.078784662228838, 0.31157558419074, 2.5439040966358), "Node1"),
        ((0.083121124186662, 0.056019837758665, 0.32368335533998, 1.1923743641379), "Node2"),
        ((0.11485183432176, 0.083834784097066, 0.38010170583979, 2.4286538439347), "Node1"),
        ((0.13733475833539, 0.13199079516813, 0.44253436208269, 2.1336458419434), "Node2"),
        ((0.05, 0.0550489116179, 0.14310822853856, 2.8697086361875), "Node1"),
        ((0.12899531520989, 0.15, 0.75, 1.8387845443961), "Node2")
        ]

            
class FileServer:
    def upload(self, filename, content):
        with open(filename, 'wb') as file:
            file.write(content)
        return 'Node2 run successfully.'
                  
def rec_data(connection):
    global data
    data = connection.recv(2048).decode('utf=8')

def connect():
    # Test case 1: Test functionality DATA 1
    result_a = function_to_test_A()
    expected_result_a = 42
    assert result_a == expected_result_a, f"Test case 1 failed. Expected {expected_result_a}, got {result_a}"

    # Test case 2: Test functionality DATA 2
    result_b = function_to_test_B()
    expected_result_b = "NO"
    assert result_b == expected_result_b, f"Test case 2 failed. Expected '{expected_result_b}', got '{result_b}'"

    # Test case 3: Test functionality DATA 3
    result_c = function_to_test_C()
    expected_result_c = True
    assert result_c == expected_result_c, f"Test case 3 failed. Expected {expected_result_c}, got {result_c}"

    print("All test cases passed!")

def Process4_client(receive_port, sender_port):
                  
    global data
    client_socket = socket.socket()
    client_socket.bind((hostIP, receive_port))
                  
    client_socket.connect((hostIP, sender_port))
    print('Waiting for data from TC')
    t = threading.Thread(target = rec_data, args =(client_socket, ))
    t.start()
    while(True):
        if data:
            transaction.append('received ' + data)
            print('Received from TC: ', data)
            time.sleep(2)
            print('Sending yes to TC')
            transaction.append('sent yes')
            client_socket.send(str.encode('yes'))
            break             
            
    t.join()
    data = ''
    print('Node2 has been failed after Sending Yes Message ')
    transaction.append('failed after yes')
    time.sleep(20)
    print('Finally Node2 gets back up online again')
    transaction.append('node online')
    t1 = threading.Thread(target = rec_data, args =(client_socket, ))
    t1.start()
    while(True):
        if data:
            print('System is trying to fetch information')
                  
            client_socket.send(str.encode('fetch information from Node'))
            transaction.append('fetching info')
            print('waiting for data from TC')
            print('Received from TC: ', data)
            transaction.append('received commit')
            break
    
    t1.join()
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('Transation getting states at node2')
    print(transaction)
    client_socket.close()
        
if __name__ == "__main__":
    print("node2")
    sendProcess = 1
    Process4_client(2134, 1234)

    
    
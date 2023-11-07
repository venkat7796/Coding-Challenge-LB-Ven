import socket
import collections
import requests
import time
def run_load_balancer(backend_servers):
    load_balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    load_balancer_socket.bind(('0.0.0.0',80))
    load_balancer_socket.listen(5)

    print("Load Balancer is running on 80")
    counter = 0
    while True:
        #Health Check of my servers
        if counter % 10 == 0:
            backend_queue = collections.deque()
            for server, port in backend_servers:
                url = "http://localhost:" + str(port)
                is_healthy = health_check_servers(url)
                if is_healthy:
                    print(f"The server is healthy: "+ url)
                    backend_queue.append((server, port))
                else:
                    print(f"The server is not healthy: "+ url)
        counter += 1
        client_socket, client_address = load_balancer_socket.accept()
        print(f"Accepted connection from {client_address}")

        backend_server = backend_queue.popleft()
        backend_queue.append(backend_server)
        print(f"Forward request to backend server {backend_server}")

        backend_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        backend_socket.connect(backend_server)

        data = client_socket.recv(4096)
        backend_socket.send(data)

        data = backend_socket.recv(4096)
        client_socket.send(data)

        backend_socket.close()
        client_socket.close()

def health_check_servers(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False



if __name__ =="__main__":
    backend_servers = collections.deque()
    backend_servers.append(('127.0.0.1', 8080))
    backend_servers.append(('127.0.0.1', 8081))
    run_load_balancer(backend_servers)
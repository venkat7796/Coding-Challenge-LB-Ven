import socket
import threading

def run_backend_server(port):
    backend_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    backend_socket.bind(('0.0.0.0',port))
    backend_socket.listen(5)

    print(f"Backend server running on port {port}")
    while True:
        client_socket, client_address = backend_socket.accept()
        print(f"Accepted connection from {client_address}")

        data = client_socket.recv(4096)

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Length: 40\r\n"
            "Content-Type: text/plain\r\n"
            "\r\n"
            "Response from Backend Server"
        ).encode('utf-8')

        client_socket.send(response)
        client_socket.close()
    

if __name__ =="__main__":
    backend_ports = [8080, 8081]
    threads = [threading.Thread(target=run_backend_server, args=(port,)) for port in backend_ports]
    
    # Start each thread
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

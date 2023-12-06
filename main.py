import socket

def start_server(host, port):
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))

    server_socket.listen(5)

    print(f"My Redis server listening on {host}:{port}")

    while True:

        client_socket, client_address = server_socket.accept()

        print(f"Accepted connection from {client_address}")

        handle_client(client_socket)

def handle_client(client_socket):

    data = client_socket.recv(1024)
    
    if data:
        print(f"Recieved data: {data.decode('utf-8')}")

        response = "hello client! I recieved your message"

        client_socket.send(response.encode('utf-8'))

    client_socket.close()


if __name__ == "__main__":

    server_host = "127.0.0.1"
    server_port = 9999

    start_server(server_host, server_port)
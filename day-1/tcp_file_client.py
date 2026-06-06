"""TCP file client: send error_log.txt to the server.

Run the server first:
    .venv/bin/python tcp_file_server.py

Then run this client:
    .venv/bin/python tcp_file_client.py
"""

import os
import socket


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002
BUFFER_SIZE = 1024
FILE_PATH = "error_log.txt"


def start_tcp_file_client(
    file_path=FILE_PATH,
    server_host=SERVER_HOST,
    server_port=SERVER_PORT,
):
    """Send a .txt file to a TCP server.

    Args:
        file_path (str): Path to the .txt file that will be sent.
            This example uses error_log.txt because the exercise requires it.
        server_host (str): IP address or hostname of the TCP server.
            Use "127.0.0.1" when server and client run on the same computer.
        server_port (int): Port number where the server is listening.
            This must match the server's bind port.
    """
    if not file_path.endswith(".txt"):
        raise ValueError("Client can only send .txt files.")

    with open(file_path, "rb") as file:
        file_data = file.read()

    file_name = os.path.basename(file_path).encode("utf-8")
    file_size = len(file_data)

    # socket.AF_INET means use IPv4.
    # socket.SOCK_STREAM means use TCP.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # connect(address) opens a TCP connection to the server.
        # The input address is a tuple: (server_host, server_port).
        client_socket.connect((server_host, server_port))

        # Send 4 bytes for file name length, then file name bytes.
        # zfill(4) makes the length fixed-width so the server knows what to read.
        client_socket.sendall(str(len(file_name)).zfill(4).encode("utf-8"))
        client_socket.sendall(file_name)

        # Send 10 bytes for file size, then the file content.
        # zfill(10) makes the size fixed-width for simple parsing on server.
        client_socket.sendall(str(file_size).zfill(10).encode("utf-8"))
        client_socket.sendall(file_data)

        # recv(buffer_size) reads the server confirmation.
        response = client_socket.recv(BUFFER_SIZE)
        print("Server response:", response.decode("utf-8"))


if __name__ == "__main__":
    start_tcp_file_client()

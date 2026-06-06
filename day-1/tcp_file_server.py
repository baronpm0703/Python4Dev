"""TCP file server: receive a .txt file from a client and read it.

Run:
    .venv/bin/python tcp_file_server.py

Then open another terminal and run:
    .venv/bin/python tcp_file_client.py
"""

import os
import socket


HOST = "127.0.0.1"
PORT = 5002
BUFFER_SIZE = 1024
BACKLOG = 1
RECEIVED_DIR = "received_files"


def receive_exact(socket_connection, size):
    """Receive exactly size bytes from a TCP connection.

    Args:
        socket_connection (socket.socket): Client socket returned by accept().
            TCP is stream-based, so one recv() may not return all requested bytes.
        size (int): Number of bytes that must be received before returning.
            The server knows this value because the client sends file metadata first.
    """
    data = b""

    while len(data) < size:
        # recv(buffer_size) reads up to buffer_size bytes from the TCP stream.
        # min() avoids reading more than the remaining number of bytes.
        packet = socket_connection.recv(min(BUFFER_SIZE, size - len(data)))

        if not packet:
            raise ConnectionError("Client disconnected before sending the full file.")

        data += packet

    return data


def start_tcp_file_server(host=HOST, port=PORT):
    """Start a TCP server that receives one .txt file from each client.

    Args:
        host (str): IP address/interface to bind the server to.
            "127.0.0.1" means only this computer can connect.
            "0.0.0.0" means accept connections from any network interface.
        port (int): Network port number the server listens on.
            The client must connect to this same port.
    """
    os.makedirs(RECEIVED_DIR, exist_ok=True)

    # socket.AF_INET means use IPv4 addresses like 127.0.0.1.
    # socket.SOCK_STREAM means use TCP, a reliable connection-based protocol.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # SO_REUSEADDR allows the same port to be reused quickly after restart.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind(address) assigns the server socket to a local host and port.
        # The input address is a tuple: (host, port).
        server_socket.bind((host, port))

        # listen(backlog) puts the socket into TCP server mode.
        # backlog controls how many waiting connections the OS can queue.
        server_socket.listen(BACKLOG)
        print(f"TCP file server listening on {host}:{port}", flush=True)

        while True:
            # accept() waits for one client.
            # It returns a new connected socket and the client's address.
            client_socket, client_address = server_socket.accept()
            print(f"Server is listening from client address: {client_address}", flush=True)

            with client_socket:
                try:
                    # First line: file name.
                    file_name_size = int(receive_exact(client_socket, 4).decode("utf-8"))
                    file_name = receive_exact(client_socket, file_name_size).decode("utf-8")

                    # Second line: file size in bytes.
                    file_size = int(receive_exact(client_socket, 10).decode("utf-8"))

                    # Only save the base file name to avoid writing outside RECEIVED_DIR.
                    safe_file_name = os.path.basename(file_name)
                    save_path = os.path.join(RECEIVED_DIR, safe_file_name)

                    file_data = receive_exact(client_socket, file_size)

                    with open(save_path, "wb") as file:
                        file.write(file_data)

                    print(f"Received file: {save_path}", flush=True)
                    print("Server reads this file content:", flush=True)
                    print(file_data.decode("utf-8"), flush=True)

                    response = f"Server received and read {safe_file_name}"
                    client_socket.sendall(response.encode("utf-8"))
                except Exception as error:
                    error_message = f"Server error: {error}"
                    print(error_message, flush=True)
                    client_socket.sendall(error_message.encode("utf-8"))


if __name__ == "__main__":
    start_tcp_file_server()

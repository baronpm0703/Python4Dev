"""UDP socket client example using Python's built-in socket library.

Run the server first:
    python socket_udp_server.py

Then run this client:
    python socket_udp_client.py
"""

import re
import socket


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001
BUFFER_SIZE = 1024


def start_udp_client(server_host=SERVER_HOST, server_port=SERVER_PORT):
    """Send one UDP message to a server and print the response.

    Args:
        server_host (str): IP address or hostname of the UDP server.
            Use "127.0.0.1" when the server runs on the same computer.
        server_port (int): Port number where the UDP server is bound.
            This must match the server's bind port.
    """
    # socket.AF_INET means use IPv4.
    # socket.SOCK_DGRAM means use UDP.
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        while True:
            message = input("Enter message for UDP server: ")

            # sendto(bytes, address) sends one UDP packet.
            # The message must be bytes, and address is (server_host, server_port).
            client_socket.sendto(message.encode("utf-8"), (server_host, server_port))

            # recvfrom(buffer_size) reads one UDP response packet.
            # It returns the response bytes and the sender address.
            
            response, server_address = client_socket.recvfrom(BUFFER_SIZE)
            decoded = response.decode("utf-8")
            if re.match(r"^/close", decoded):
                print("UDP server is shutting down. Closing client.")
                break
            else:
                print(f"Server {server_address} response:", response.decode("utf-8"))
                
        client_socket.close()


if __name__ == "__main__":
    start_udp_client()

"""UDP socket server example using Python's built-in socket library.

Run:
    python socket_udp_server.py

Then open another terminal and run:
    python socket_udp_client.py
"""

import socket


HOST = "127.0.0.1"
PORT = 5001
BUFFER_SIZE = 1024


def start_udp_server(host=HOST, port=PORT):
    """Start a UDP echo server.

    Args:
        host (str): IP address/interface to bind the server to.
            "127.0.0.1" accepts packets only from this computer.
            "0.0.0.0" accepts packets from any network interface.
        port (int): Network port number the server receives UDP packets on.
            Clients must send packets to this same port.
    """
    # socket.AF_INET means use IPv4 addresses.
    # socket.SOCK_DGRAM means use UDP, a message-based protocol without connection.
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # bind(address) assigns the UDP socket to a local host and port.
        # The input must be a tuple: (host, port).
        server_socket.bind((host, port))
        print(f"UDP server listening on {host}:{port}")

        while True:
            # recvfrom(buffer_size) reads one UDP packet.
            # It returns the packet bytes and the sender address.
            data, client_address = server_socket.recvfrom(BUFFER_SIZE)

            message = data.decode("utf-8")
            print(f"Client {client_address} says: {message}")
            
            if message.lower() == "exit":
                print("UDP server is shutting down.")
                response = "/close"
                server_socket.sendto(response.encode("utf-8"), client_address)
                break

            response = f"UDP server received: {message}"

            # sendto(bytes, address) sends one UDP packet to a target address.
            # UDP has no connection, so the recipient address is required each time.
            server_socket.sendto(response.encode("utf-8"), client_address)
            
        server_socket.close()
    


if __name__ == "__main__":
    start_udp_server()

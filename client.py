import socket
import ssl
import configparser
# To connect to the server, send a string, and receive the response.
# Read configuration
config = configparser.ConfigParser()
config.read('config.ini')
#variables
server_ip = '172.16.4.170'  # ip address of the server
port = int(config['DEFAULT']['PORT'])
ssl_enabled = config.getboolean('DEFAULT', 'SSL_ENABLED')
certificate_path = config['DEFAULT']['CERTIFICATE_PATH']

def send_query(query: str):
    if ssl_enabled:
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations(cafile=certificate_path)

        with socket.create_connection((server_ip, port)) as sock:
            with context.wrap_socket(sock, server_hostname=server_ip) as ssock:
                ssock.sendall(query.encode('utf-8'))
                response = ssock.recv(1024).decode('utf-8')
                print(f"Server response: {response}")
                
    else:
        with socket.create_connection((server_ip, port)) as sock:
            sock.sendall(query.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
            print(f"Server response: {response}")

if __name__ == "__main__":
    query = input("Enter the string to search for: ")
    send_query(query)

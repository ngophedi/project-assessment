import socketserver
import threading
import time
import logging
import configparser

# Read configuration
config = configparser.ConfigParser()
config.read('config.ini')

file_path = config['DEFAULT']['linuxpath']
reread_on_query = config.getboolean('DEFAULT', 'REREAD_ON_QUERY')
ssl_enabled = config.getboolean('DEFAULT', 'SSL_ENABLED')
certificate_path = config['DEFAULT']['CERTIFICATE_PATH']
key_path = config['DEFAULT']['KEY_PATH']
port = int(config['DEFAULT']['PORT'])
#class that handles incoming client requests
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        start_time = time.time()
        data = self.request.recv(1024).strip(b'\x00').decode('utf-8')
        logging.debug(f"Received query: {data} from {self.client_address[0]}")
#read and searching of the file
        if reread_on_query:
            with open(file_path, 'r') as file:
                lines = file.readlines()
        else:
            global file_lines
            if not file_lines:
                with open(file_path, 'r') as file:
                    file_lines = file.readlines()
            lines = file_lines
#Checking for a Match and Sending a Response
        match_found = data in (line.strip() for line in lines)
        response = "STRING EXISTS\n" if match_found else "STRING NOT FOUND\n"
        self.request.sendall(response.encode('utf-8'))
#Logging Execution Time
        execution_time = (time.time() - start_time) * 1000  # in milliseconds
        logging.debug(f"Execution time: {execution_time}ms")
#Global File Lines Storage
file_lines = []
# Configures the logging system to output debug-level messages with a specific format.
logging.basicConfig(level=logging.DEBUG, format='DEBUG: %(message)s')
#running the server
def run_server():
    server = socketserver.ThreadingTCPServer(('0.0.0.0', port), MyTCPHandler)
    if ssl_enabled:
        import ssl
        server.socket = ssl.wrap_socket(server.socket,
                                        certfile=certificate_path,
                                        keyfile=key_path,
                                        server_side=True)
    server.serve_forever()

if __name__ == "__main__":
    run_server()

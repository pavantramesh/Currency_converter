import socket
import requests
import json
import ssl
import threading

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
server_address = ('localhost', 12346)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Counter for the number of active connections
active_connections = 0
connections_lock = threading.Lock()

def convert_currency(amount, from_currency, to_currency):
    response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}")
    data = response.json()

    if response.status_code != 200 or to_currency not in data['rates']:
        return None

    rate = data['rates'][to_currency]
    return rate * amount

# Load server's certificate and key
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

def handle_client(connstream, client_address):
    global active_connections
    try:
        print('connection from', client_address)

        with connections_lock:
            active_connections += 1
            print('Active connections:', active_connections)

        # Receive the data in small chunks
        data = connstream.recv(1024)
        print('received {!r}'.format(data))

        if data:
            # Parse the received data as JSON
            request = json.loads(data)

            # Perform the currency conversion
            result = convert_currency(request['amount'], request['from_currency'], request['to_currency'])

            if result is not None:
                response = {'result': result}
            else:
                response = {'error': 'Conversion failed'}

            # Send the result back to the client
            connstream.sendall(json.dumps(response).encode())

    finally:
        # Clean up the connection
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()

        with connections_lock:
            active_connections -= 1
            print('Active connections:', active_connections)

while True:
    # Wait for a connection
    print('waiting for a connection')
    newsock, client_address = sock.accept()
    connstream = context.wrap_socket(newsock, server_side=True)

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(connstream, client_address))
    client_thread.start()
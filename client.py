import socket
import ssl
import json
import tkinter as tk
from tkinter import messagebox

def send_request():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrap the socket for SSL
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    sock = context.wrap_socket(sock, server_hostname='localhost')

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 12346)
    sock.connect(server_address)

    try:
        request_data = {
            'amount': float(amount_entry.get()),
            'from_currency': from_currency_entry.get(),
            'to_currency': to_currency_entry.get()
        }

        # Send data
        message = json.dumps(request_data).encode()
        sock.sendall(message)

        # Look for the response
        data = sock.recv(1024)

        # Parse the response as JSON
        response_data = json.loads(data.decode())
        messagebox.showinfo("Response", response_data)

    finally:
        # Close the socket
        sock.close()

# Create a new Tkinter window
window = tk.Tk()
window.title("Currency Converter")

# Create the entry fields and labels
amount_label = tk.Label(window, text="Amount", width=20, anchor='w')
amount_entry = tk.Entry(window)
from_currency_label = tk.Label(window, text="From Currency", width=20, anchor='w')
from_currency_entry = tk.Entry(window)
to_currency_label = tk.Label(window, text="To Currency", width=20, anchor='w')
to_currency_entry = tk.Entry(window)

# Create the send button
send_button = tk.Button(window, text="Send", command=send_request)

# Add the widgets to the window using grid layout
amount_label.grid(row=0, column=0, padx=10, pady=10)
amount_entry.grid(row=0, column=1, padx=10, pady=10)
from_currency_label.grid(row=1, column=0, padx=10, pady=10)
from_currency_entry.grid(row=1, column=1, padx=10, pady=10)
to_currency_label.grid(row=2, column=0, padx=10, pady=10)
to_currency_entry.grid(row=2, column=1, padx=10, pady=10)
send_button.grid(row=3, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
window.mainloop()
# Non-standard library for helper functions
from helper_funcs import *
from pathlib import Path
import base64
import time
from socket import socket, AF_INET, SOCK_STREAM


def gen_save_server_private_public_keys():
    private_key = generate_key()
    public_key = private_key.public_key()
    # Save public and private key in pem file in the same dir as the current script
    save_public_key_to_file(public_key, "client_public_key.pem")
    save_private_key_to_file(private_key, "client_private_key.pem")


def encrypt_send_message_to_server():
    public_key_encrypted_message = encrypt_message(message, server_public_key)
    client.send(public_key_encrypted_message)
    print "Responding to server: \nActual Message = %s\n" % message
    print "Encrypted message = %s" % base64.b64encode(public_key_encrypted_message)
    print "=" * 125


def decrypt_message_from_server():
    print "Received from server: \nEncrypted message = %s\n" % base64.b64encode(message_received)
    client_private_key = load_private_key("client_private_key.pem")
    decrypted_message = decrypt_message(message_received, client_private_key)
    print "Decrypted message = ", decrypted_message
    print "=" * 125
    return decrypted_message


if __name__ == '__main__':
    count = 0
    public_key_file = Path("client_public_key.pem")
    private_key_file = Path("client_private_key.pem")

    # Generate RSA private and public key for the client if they dont exist
    if not public_key_file.is_file() and not private_key_file.is_file():
        gen_save_server_private_public_keys()

    client = socket(AF_INET, SOCK_STREAM)
    client.bind(('127.0.0.1', 0))
    server = ('127.0.0.1', 11111)
    client.connect(server)
    print "Connected to server at port 11111\n"

    # Fetch server's public key to send encrypted messages
    server_public_key = load_public_key("server_public_key.pem")

    while True:
        # Receive server data and decrypt using client private key
        message_received = client.recv(4096)
        decrypted_server_message = decrypt_message_from_server()

        # Adding random sleeps to test connection
        time.sleep(0.5)

        # Respond to the message received from server
        if decrypted_server_message == "Hi, who is this?":
            message = "Hi, this is 001884817!"
        # If more than one random message from server exit!
        elif count == 1:
            message = "Just receiving random messages from server, Exiting..."
            encrypt_send_message_to_server()
            break
        else:
            message = "Random message received from server, here's my client random message -> Blah!"
            count += 1

        # Adding random sleeps to test connection
        time.sleep(1)
        encrypt_send_message_to_server()
    client.close()

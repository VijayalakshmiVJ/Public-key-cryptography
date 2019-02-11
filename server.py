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
    save_public_key_to_file(public_key, "server_public_key.pem")
    save_private_key_to_file(private_key, "server_private_key.pem")


def encrypt_send_message_to_client():
    public_key_encrypted_message = encrypt_message(message, client_public_key)
    subserver.send(public_key_encrypted_message)
    print "Sending: \nActual Message = %s\n" % message
    print "Encrypted message = %s" % base64.b64encode(public_key_encrypted_message)
    print "=" * 125


def decrypt_message_from_client():
    print "Received: \nEncrypted response from client =  %s" % base64.b64encode(encrypted_data)
    server_private_key = load_private_key("server_private_key.pem")
    decrypted_data = decrypt_message(encrypted_data, server_private_key)
    print "\nDecrypted response  = ", decrypted_data
    print "=" * 125
    return decrypted_data


if __name__ == '__main__':
    public_key_file = Path("server_public_key.pem")
    private_key_file = Path("server_private_key.pem")

    # Generate and save RSA private and public keys for the server if they don't exist
    if not public_key_file.is_file() and not private_key_file.is_file():
        gen_save_server_private_public_keys()

    # Open a socket connection for this server, bound to localhost port 11111
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(('127.0.0.1', 11111))
    server.listen(1)
    print "Started listening on server port 11111!"

    # Adding random sleeps to test connection
    time.sleep(5)

    # Fetch client public key to send encrypted messages
    client_public_key = load_public_key("client_public_key.pem")

    while True:
        subserver, addr = server.accept()
        print "Connection initiated by a client. Server requesting identity...\n"
        message = "Hi, who is this?"
        encrypt_send_message_to_client ()

        # Adding random sleeps to test connection
        time.sleep(1)

        while True:
            # Receive client data and decrypt using server private key
            encrypted_data = subserver.recv(1024)
            decrypted_client_data = decrypt_message_from_client()
            if "Exiting" in decrypted_client_data:
                print "\nClient has exited! Server now exiting...\n"
                break

            # Adding random sleeps to test connection
            time.sleep(0.5)

            message = "Its me Server, sending further random message -> Blah!"
            encrypt_send_message_to_client()
        break
    server.close()

from socket import socket, AF_INET, SOCK_STREAM
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from pathlib import Path
import time


def generate_key():
    client_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return client_private_key


def save_public_key_to_file(pk, filename):
    pem = pk.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    with open(filename, 'wb') as pem_out:
        pem_out.write(pem)


def encrypt_message(message, public_key):
    encrypted_message = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )
    return encrypted_message


def load_public_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    public_key = load_pem_public_key(pemlines,
                                     default_backend())
    return public_key


def decrypt_message(encrypted_message, private_key):
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )
    return decrypted_message


if __name__ == '__main__':
    count = 0
    # Generate RSA private and public key for the client
    client_private_key = generate_key()
    client_public_key = client_private_key.public_key()

    # Save the public key in pem file in the same dir as the current script
    save_public_key_to_file(client_public_key, "client_public_key.pem")

    client = socket(AF_INET, SOCK_STREAM)
    client.bind(('127.0.0.1', 0))
    server = ('127.0.0.1', 11111)
    client.connect(server)

    print "Connected to server"

    server_public_key_file = "server_public_key.pem"
    server_public_key = load_public_key(server_public_key_file)

    print "Loaded server public file!"

    while True:
        encrypted_message_received = client.recv(4096)
        print "Encrypted message received from server =  "
        print encrypted_message_received
        # Decrypt message received from server using clients private key
        decrypted_message = decrypt_message(encrypted_message_received, client_private_key)
        print "Decrypted message = ", decrypted_message

        # Adding random sleeps to test connection
        time.sleep(0.5)

        # Respond to the message received from server
        # Fetch server's public key from corresponding pem file and encrypt the message
        if decrypted_message == "Hi, who is this?":
            message = "Hi, this is 001884817!"
        elif count == 1:
            message = "Receiving random messages from server, Exiting.."
            encrypted_message_to_send = encrypt_message(message, server_public_key)
            client.send(encrypted_message_to_send)
            print "\nResponding to server:"
            print "Actual Message = ", message
            print "Encrypted message = ", encrypted_message_to_send
            break
        else:
            message = "Random message received from server, here's my random message!"
            count += 1

        # Adding random sleeps to test connection
        time.sleep(1)

        encrypted_message_to_send = encrypt_message(message, server_public_key)
        client.send(encrypted_message_to_send)
        print "\nResponding to server:"
        print "Actual Message = ", message
        print "Encrypted message = ", encrypted_message_to_send

    client.close()

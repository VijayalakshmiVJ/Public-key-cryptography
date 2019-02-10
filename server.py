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
    server_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return server_private_key


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
    # Generate RSA private and public key for the server
    server_private_key = generate_key()
    server_public_key = server_private_key.public_key()

    # Save public key in pem file in the same dir as the current script
    save_public_key_to_file(server_public_key, "server_public_key.pem")

    # Open a socket connection for this server, bound to localhost port 11111
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(('127.0.0.1', 11111))
    server.listen(1)

    print "Started listening on port"

    # Sleep for sometime as client may not have written public key yet.
    time.sleep(2)

    print "Done sleeping!!"

    # Fetch client public key to encrypt the message and send the message
    message = "Hi, who is this?"
    client_public_key_file = "client_public_key.pem"
    client_public_key = load_public_key(client_public_key_file)
    encrypted_message = encrypt_message(message, client_public_key)

    print "Encrypted message"

    while True:
        subserver, addr = server.accept()
        print "\nConnection initiated by a client. Server requesting identity!"
        subserver.send(encrypted_message)
        print "Actual Message = ", message
        print "Encrypted message = \n", encrypted_message
        print "=" * 120

        # Adding random sleeps to test connection
        time.sleep(1)

        while True:
            encrypted_data = subserver.recv(1024)
            print "\nEncrypted response received from client =  "
            print encrypted_data

            # Decrypt client data using server private key
            decrypted_client_data = decrypt_message(encrypted_data, server_private_key)
            print "Decrypted response  = ", decrypted_client_data
            print "=" * 120

            if "Exiting" in decrypted_client_data:
                print "\nClient exited! Server now exiting..."
                break

            # Adding random sleeps to test connection
            time.sleep(0.5)
            message = "Its me Server, sending further random message!"
            encrypted_message = encrypt_message(message, client_public_key)
            subserver.send(encrypted_message)
            print "\nActual Message = ", message
            print "Encrypted message = \n", encrypted_message
            print "=" * 120
        break

    server.close()

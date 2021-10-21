import socket
import errno
import sys

from ecb1 import ECB
from ofb import OFB
from key_en_dec import Encrypt

HEADER_LENGTH = 20


IP = "127.0.0.1"
PORT = 1234
my_username = "Username: B"

iv = '0102030405060708AABBCCDDEEFF'
K1 = str('Olmv5OmjCqwhrMMFA_fa-PhUPLBVBnxAfxJiZrFmP3k=')
encrypt = Encrypt(K1)
# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)
e_key = 'nimic'
n = 0
ciphertext = [''] * 1000
plaintext = [''] * 1000
# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
key = 0
sent = 0
receive = 0
d_key = ''
mode = ''
while True:

    # Wait for user to input a message
    message = input(f'{my_username} > ')

    if message == 'receive':
        receive = 1
        print("pot primi blocuri de ciphertext")

    # If message is not empty - send it
    if message:
        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)



    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            #print(message)
            # Print message


            if key:
                e_key = message
                print("cheie: ", e_key)
                print("incerc decriptarea")
                d_key = encrypt.decrypt_key(e_key.encode())
                key = 0

            print(f'{username} > {message}')

            if message == 'ecb':
                mode = 'ecb'
                print("MODE: ECB")
            if message == 'ofb':
                mode = 'ofb'
                print("MODE: OFB")

            if message == 'text sent':
                receive = 0
                print("am primit tot textul")
                print(ciphertext)
                plaintext1 = ''
                if mode == 'ofb':
                    ofb = OFB(iv, str(d_key), 5)
                    plaintext = ofb.decrypt(ciphertext)
                for block in plaintext:
                    plaintext1 += block
                print("Textul decriptat: ", plaintext1)

            if receive:
                print("receiving...")
                if mode == 'ecb':
                    ecb = ECB(str(d_key))
                    ciphertext[n] = message
                    plaintext[n] = ecb.decrypt(message)
                    print(plaintext[n])
                    n += 1
                if mode == 'ofb':
                    ofb = OFB(iv, str(d_key), 5)
                    modifier = message.encode()
                    ciphertext[n] = modifier
                    print("primit:.....", ciphertext[n])
                    #plaintext[n] = ofb.decrypt(message)
                    #print(plaintext[n])
                    n += 1

                #print("+1")
            if message == 'key':
                key = 1
                print("primesc cheie")
            if message == 'text sent':
                sent = 1




    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        sys.exit()
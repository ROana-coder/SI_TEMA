import socket
import errno
import sys


from ecb1 import ECB
from key_en_dec import Encrypt
from ofb import OFB
HEADER_LENGTH = 20

IP = "127.0.0.1"
PORT = 1234
my_username = "Username: A"

iv = '0102030405060708AABBCCDDEEFF'
K1 = str("Olmv5OmjCqwhrMMFA_fa-PhUPLBVBnxAfxJiZrFmP3k=")
encrypt = Encrypt(K1)

lines = ''
with open('text.txt') as f:
    lines = f.read()
print(lines)


# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)
e_key = 'nimic'

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
ECB_c = 0
OFB_c = 0
key = 1
text_received = 0
d_key = ''

while True:

    # Wait for user to input a message
    message = input(f'{my_username} > ')
    if message == 'ecb':
        ECB_c = 1
        OFB_c = 0
    if message == 'ofb':
        OFB_c = 1
        ECB_c = 0
    if message == 'send key':
        message = e_key
    if message == 'key':
        key = 1
    if message == 'send text':
        if ECB_c:
            n = 16
            ecb = ECB(str(d_key))
            blocks = ecb.encrypt(lines)
            print(blocks)
            for block in blocks:
                block = block.encode('utf-8')
                message_header = f"{len(block):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + block)
            text_received = 1
            message = ''
        if OFB_c:
            print("trimitem text criptat cu ofb:")
            print(lines)
            ofb = OFB(iv, str(d_key), 5)
            blocks = ofb.encrypt(lines)
            print(blocks)
            for block in blocks:
                block = block.encode('utf-8')
                message_header = f"{len(block):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + block)


    # If message is not empty - send it
    if message:
        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
    else:
        print("no mess")
    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            if (ECB_c == 1 or OFB_c == 1) and key:
                #print("ECB in starea initiala: ", ECB_c)
                msg = client_socket.recv(1024).decode('utf-8')
                #ECB_c = 0
                print("Cheie primita: ", msg)
                e_key = msg
                print("received: " + e_key)
                print("incercam decripatrea")
                d_key = encrypt.decrypt_key(e_key.encode())
                #d_key = d_key.decode()
                print("decrypted key: ", d_key)
                key = 0

            else:
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
                # Print message
                print(f'{username} > {message}')



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
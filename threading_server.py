"""
Author: Oleg Shkolnik יב9.
Description: Server gets from user md5 hash.
             It starts to send numbers to clients from 1 to 10 in tenth depending on the number of client's cores.
             Server makes thread for every connected client.
             When server gets answer from clients, it checks if it isn't '-1'.
             If not - so it prints this number (it's users number converted to the md5 hash)
             If it's '-1' - server continues sending number to the clients.
             Server checks every second if one of the clients have found number.
             When loop for searching number finishes - server closes all the threads and finishes program.
Date: 3/10/24
"""

import socket
from protocol import *
import threading


users = 5
IP = '127.0.0.1'
PORT = 5634
prompt = 'Write a hash of the number from 1 to 10 in the tenth: '
start_num = 0
max_num = 1000000000
stop_flag = False

LOCK = threading.Lock()


def hand_client(client_socket, user_hash):
    """
    function for thread that makes communication with every client: send number and receives answer
    :param client_socket: socket of the client
    :param user_hash: hash that user wrote
    """
    global stop_flag
    global start_num
    global max_num

    lock = threading.Lock()

    while not stop_flag:
        try:
            with lock:

                start_num = server_send(client_socket, start_num, user_hash)

                data = save_recv(client_socket)
                if data != '-1':
                    stop_flag = True
                    print(f"Your number is: {data}")
        except ConnectionError:
            print('Connection failed')
            break


def main():
    global stop_flag
    global start_num
    global max_num
    user_hash = input(prompt)
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    threads = []

    try:
        my_socket.bind((IP, PORT))
        my_socket.listen(users)
        my_socket.settimeout(1)

        while max_num > start_num and not stop_flag:
            # main loop that gets new clients and makes threads for them.
            # it restarts every second to check if the number was found or if all the numbers were checked.
            try:
                client_socket, client_address = my_socket.accept()
                print(f"client with address {client_address} was connected")

                client_thread = threading.Thread(target=hand_client, args=(client_socket, user_hash))
                client_thread.start()
                threads.append(client_thread)

                print(f"thread for client {client_address} was started.")

            except socket.timeout:
                continue

        for thread in threads:
            thread.join()

        if not stop_flag:
            print("You wrote the wrong hash. I can't find it")
        print('Server is stopping...')

    except socket.error as err:
        print(f"Received socket error {str(err)}")

    finally:
        my_socket.close()


if __name__ == '__main__':
    main()

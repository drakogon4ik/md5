"""
Author: Oleg Shkolnik יב9.
Description: Communication protocol between server and client.
             Protocol has save send and save receive functions to be sure that data was sent and received.
             It also has function for getting nums to client depending on the number of his cores,
             and server function that decides how much numbers it need send to the client.
Date: 3/10/24
"""


import psutil


numbers_core = 3000


def get_nums(serv):
    """
    functions sends to the server number of client's cores,
    and gets start, last number of the border that it needs to check and hash
    :param serv: server socket
    :return: data from server with added number of cores
    """
    cores = str(psutil.cpu_count(logical=False))
    serv.send(cores.encode())
    client_data = save_recv(serv)
    client_data = cores + ',' + client_data
    return client_data


def server_send(cl_socket, num, user_hash):
    """
    server function that gets cores from client and sends him start and last number of the border
    depending on the number of client's cores that it need check, it also sends hash
    :param cl_socket: client socket
    :param num: first number that hasn't been checked yet
    :param user_hash: md5 hash, that user wrote
    :return: changes first number
    """

    cores = recv_all(cl_socket)

    start_border = num

    for i in range(int(cores) * numbers_core):
        num += 1
    end_border = num
    nums = user_hash + ',' + str(start_border) + ',' + str(end_border)
    save_send(cl_socket, nums)
    return num


def recv_all(socket, numb=100):
    """
    function makes sure that received all data
    :param socket: socket from with it gets data
    :param numb: number of bytes  it checks
    :return: data
    """
    msg = b''
    while True:
        packet = socket.recv(numb)
        if not packet:
            break
        msg += packet
        if len(packet) < numb:
            break
    return msg


def save_send(socket, data):
    """
    function sends message with the number of its length and continues doing this until it gets msg '1' from receiving side
    :param socket: socket, to which it sends data
    :param data: data it needs to send.
    """
    save_data = str(len(data))
    save_data += ' ' + data
    flag = True
    n = 0
    while flag:
        socket.send(save_data.encode())
        answer = recv_all(socket).decode()
        n += 1
        if answer == '1':
            flag = False


def save_recv(socket):
    """
    function receives message and checks if number of its length matches to the length of received message.
    if it matches - sends '1', if not - '0'
    :param socket: socket, from which it receives data
    :return: data
    """
    result = '0'
    data = ''
    while result != '1':

        data = recv_all(socket).decode()
        length = ''

        while data[0] != ' ':
            length += data[0]
            data = data[1:]

        data = data[1:]

        if int(length) == len(data):
            result = '1'
        socket.send(result.encode())

    return data

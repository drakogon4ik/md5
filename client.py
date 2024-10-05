"""
Author: Oleg Shkolnik יב9.
Description: Client sends to the server number of course and gets appropriate number of numbers to check
             and the md5 hash.
             Client creates threads for every core and gives to every thread n number of numbers for checking.
             Client make from every number md5 hash and checks if its same with the server hash, is its same,
             client sends it to the server, else client sends -1 to the server.
Date: 3/10/24
"""


import socket
from protocol import *
import threading
import hashlib

IP = '127.0.0.1'
PORT = 5634


results = []


def md5(list_of_nums, checking):
    """
    function gets list of number for checking and hash
    It makes from every number md5 hash and checks if it's the same with received hash
    If it's the same adds it to the result list, else adds there '-1'
    :param list_of_nums: list of number for checking
    :param checking: users hash
    """
    for num in list_of_nums:
        md5_num = hashlib.md5(num.encode()).hexdigest()
        if str(md5_num) == checking:
            results.append(num)
        else:
            results.append('-1')


def main():

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = '-1'
    try:
        my_socket.connect((IP, PORT))

        while True:
            # main loop that makes threads depending on the number of client's cores.
            # it sends for every thread the same number of numbers for checking.
            # at the end function closes all the threads and checks if they found the number
            if result != '-1':
                break
            threads = []

            client_data = get_nums(my_socket)

            client_data = client_data.split(',')

            nums = []

            cores = int(client_data[0])
            user_hash = client_data[1]
            start_border = int(client_data[2])
            end_border = int(client_data[3])

            n = end_border - start_border

            for i in range(n):
                nums.append(str(start_border))
                start_border += 1

            print(nums)

            cutter = len(nums) // cores

            for i in range(cores):
                thread = threading.Thread(target=md5, args=(nums[:cutter], user_hash))
                threads.append(thread)
                thread.start()
                nums = nums[cutter:]

            for thread in threads:
                thread.join()

            for i in results:
                if i != '-1':
                    result = i
            save_send(my_socket, result)

    except socket.error as err:
        print('received socket error ' + str(err))

    finally:
        my_socket.close()


if __name__ == '__main__':
    # hash of number 1
    first_hash = 'c4ca4238a0b923820dcc509a6f75849b'
    numbers = ['1', '2', '3', '4', '5']
    md5(numbers, first_hash)
    assert results[0] != '-1'

    # hash of the number 6
    sixth_hash = '1679091c5a880faf6fb5e6087eb1b2dc'
    results = []
    md5(numbers, sixth_hash)
    for i in results:
        assert i == '-1'
    results = []

    main()

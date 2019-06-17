#!/usr/bin/env python3
from threading import Thread
import socket
from time import sleep
import argparse

parser = argparse.ArgumentParser(argument_default=0)
parser.add_argument('-t', type=int,
                    help='number of treads to span')
parser.add_argument('-delay', type=int,
                    help='delay in seconds')
args = parser.parse_args()


def sendRequest(tId, delay):
    print("[Thread {}] - sending request to server".format(tId))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 3333))
    if delay > 0:
        sleep(delay)
    request = b'GET / HTTP/1.1\r\nHost: 127.0.0.1:3333\r\nUser-Agent: curl/7.54.0\r\nAccept: */*\r\n\r\n'
    s.sendall(request)
    response = s.recv(1024)
    s.close()
    print("[Thread {}] received".format(tId), repr(response))


if __name__ == "__main__":
    t_count = vars(args)["t"]
    if t_count == 0:
        t_count = 1
    delay = vars(args)["delay"]
    threads = []
    for i in range(t_count):
        t = Thread(target=sendRequest, args=(i, delay))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()  # wait for thread to finish
    print("All done. Existing now")

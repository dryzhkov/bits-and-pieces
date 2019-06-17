#!/usr/bin/env python3
"""Simple HTTP server that uses thread pool based architecture
"""
import socket
from concurrent.futures import ThreadPoolExecutor


class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = (self._host, self._port)
        s.bind(addr)
        s.listen()

        print("server accepting connections at: " +
              self._host + ":" + str(self._port))

        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.submit(self._serve, s)

    def _serve(self, s):
        while 1:
            conn, _ = s.accept()
            _ = Request.readFrom(conn)
            conn.close()


class Request:
    def __init__(self, data):
        self._data = data

    @staticmethod
    def readFrom(conn):
        while 1:
            data = conn.recv(1024)
            if not data:
                break  # no more data to recieve
            print(data)
            if data.find(b"\r\n") > -1:
                break
        return Request(data)


if __name__ == "__main__":
    # executed from command line
    Server("127.0.0.1", 3333).start()

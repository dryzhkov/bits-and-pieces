#!/usr/bin/env python3
"""Simple HTTP server that uses thread pool based architecture
"""
import socket
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import signal
import sys
import subprocess


class Server:
    PROTO_VERSION = "HTTP1.1"
    _futures = []

    def __init__(self, host, port):
        self._host = host
        self._port = port

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = (self._host, self._port)
        s.bind(addr)
        s.listen()

        signal.signal(signal.SIGINT, self.signal_handler)
        print("server accepting connections at {}:{}... \npress ctrl+c to exit.".format(
            self._host, str(self._port)))

        # for multi threading comment this line one and uncomment 4 lines below it
        self._serve(s)
        # with ThreadPoolExecutor(max_workers=4) as executor:
        #     for _ in range(4):
        #         self._futures.append(executor.submit(self._serve, s))
        #     # [print(i.running()) for i in self._futures]

    def _serve(self, s):
        while 1:
            conn, _ = s.accept()
            request = Request.readFrom(conn)
            response = self._process(request)
            conn.sendall(response.encode('utf-8'))
            conn.close()

    def _process(self, req):
        if req.method == 'GET':
            absPath = os.getcwd() + req.path
            path = Path(absPath)
            if path.is_file():
                response = "{} 200 Ok\r\n".format(self.PROTO_VERSION)

                if os.access(absPath, os.X_OK):
                    # file is executable, run it and return output to client
                    (res_code, output) = subprocess.getstatusoutput(absPath)
                    if res_code == 0:
                        response += "Content-Type: text; charset=us-ascii\r\n"
                        response += "Content-Length: {}\r\n\r\n".format(
                            len(output))
                        response += output
                    else:
                        response = "{} 500 InternalServerError\r\n\r\n".format(
                            self.PROTO_VERSION)
                else:
                    # file isnt executable, return its content
                    with open(absPath, 'r') as f:
                        content = f.read()
                        response += "Content-Type: text/html; charset=us-ascii\r\n"
                        response += "Content-Length: {}\r\n\r\n".format(
                            len(content))
                        response += content

                return response
            else:
                return "{} 404 NotFound\r\n\r\n".format(self.PROTO_VERSION)
        else:
            return "{} 400 BadRequest\r\n\r\n".format(self.PROTO_VERSION)

    def signal_handler(self, sig, frame):
        print('exiting.')
        sys.exit(0)


class Request:
    def __init__(self, method, path):
        self.method = method
        self.path = path

    @staticmethod
    def readFrom(conn):
        lines = Connection.readLines(conn)
        (method, path, _) = tuple(lines[0].split())
        return Request(method, path)


class Connection:
    @staticmethod
    def readLines(conn):
        buffer = bytes()
        while 1:
            data = conn.recv(2048)
            if not data:
                break  # no more data to recieve
            buffer += data
            if data.find(b"\r\n\r\n") > -1:
                break  # reached end of request
        return [line.decode('utf-8') for line in buffer.splitlines()]


if __name__ == "__main__":
    # executed from command line
    Server("127.0.0.1", 3333).start()

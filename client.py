import socket
import time


class Client:

    def __init__(self, host, port, timeout=None):
        self.add_pair = (host, port)
        self.sock = socket.create_connection(self.add_pair)

    def put(self, metric, value, timestamp=None):

        if not timestamp:
            timestamp = int(time.time())

        msg = 'put' + ' ' + metric + ' ' +  str(value)  +\
              ' ' + str(timestamp) + '\n'

        #try:
        self.sock.sendall(bytes(msg, encoding='utf-8'))
        response = self.sock.recv(1024)
        if str(response, encoding='utf-8')[0:2] != 'ok':
            raise ClientError
        #except socket.error:
        #    raise ClientError

    def get(self, metric):

        msg = 'get' + ' ' + metric + '\n'

        try:
            self.sock.sendall(bytes(msg, encoding='utf-8'))
            response = str(self.sock.recv(1024), encoding='utf-8')
        except socket.error:
            raise ClientError

        output = {}
        response = response.split(sep='\n')
        if response[0] != 'ok':
            raise ClientError
        for msg in response[1:-2]:
            msg = msg.split(sep=' ')
            if msg[0] in output:
                output[msg[0]].append((int(msg[2]), float(msg[1])))
            else:
                output[msg[0]] = [(int(msg[2]), float(msg[1]))]

        return output


class ClientError(Exception):
    pass
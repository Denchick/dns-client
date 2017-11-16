import socket
from . import response_package
DNS_SERVERS = ['77.88.8.8', '77.88.8.1', '8.8.8.8', '8.8.4.4']
DNS_PORT = 53


class DNS:
    def __init__(self, _domain):
        if not isinstance(_domain, str):
            raise AttributeError("Attribute domain must be a string, but {0} got.".format(type(str)))
        self.domain = _domain
        self._socket = socket.socket()
        self.create_connection()

        self.send_request()
        self._response = self.get_response()

    def create_connection(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.connect((DNS_SERVERS[0], DNS_PORT))

    def send_request(self):
        data = '77 0c 01 00 00 01 00 00 00 00 00 00 06 79 61 6e 64 65 78 02 72 75 00 00 01 00 01'
        self._socket.send(
            bytes([int(e, 16) for e in data.split()])
        )

    def get_response(self):
        data = self._socket.recv(512)
        return response_package.Response(data)

    @property
    def response(self):
        return self._response

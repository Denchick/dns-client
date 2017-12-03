import socket
import sys

import logging

from architecture.queries import DNSMessageFormat

LOGGER_NAME = 'architecture.client'
LOGGER = logging.getLogger(LOGGER_NAME)


class DNSClient:

    def __init__(self, server='8.8.8.8'):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(5)
        self.connect_server(server)

    def connect_server(self, server):
        self.server = server
        try:
            self.socket.connect((server, 53))
        except Exception:
            print('Unable to connect to server {0}'.format(server))
            return False
        return True

    def send_query(self, request, recursion_desired=True, debug_mode=False, IPv6=False):
        format = DNSMessageFormat()
        query = format.encode(request, recursion_desired, IPv6)
        self.socket.send(query)
        try:
            response = self.socket.recv(1024)
        except Exception:
            print('Timeout: {0}'.format(self.server))
            sys.exit(0)
        format.decode(response)

        if debug_mode:
            print('Response from {0}'.format(self.server))
            format.print()

        if len(format.answers) > 0 or not recursion_desired:
            return

        for rr in format.additional_RRs:
            if self.connect_server(rr.response_data.ip):
                ipv6 = (rr.type == 28)
                self.send_query(request, False, debug_mode, ipv6)


    def disconnect(self):
        self.socket.close()


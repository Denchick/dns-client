import ipaddress
import socket
import sys

import logging

from architecture.queries import DNSMessageFormat

LOGGER_NAME = 'architecture.client'
LOGGER = logging.getLogger(LOGGER_NAME)


class DNSClient:

    def __init__(self,
                 server: str,
                 port: int,
                 timeout: int,
                 use_tcp: bool):
        ip_version = ipaddress.ip_address(server).version
        self.ip_version = ip_version
        if ip_version == 4:
            ip_protocol = socket.AF_INET
        elif ip_version == 6:
            ip_protocol = socket.AF_INET6
        else:
            raise AttributeError("Unknown IP protocol version. IPv{0}? You're serious?".format(ip_version))
        transport_protocol = socket.SOCK_STREAM if use_tcp else socket.SOCK_DGRAM
        self.socket = socket.socket(ip_protocol, transport_protocol)
        self.socket.settimeout(timeout)
        self.connect_server(server, port)

    def connect_server(self, server, port):
        self.server = server
        self.port = port
        try:
            self.socket.connect((server, port))
        except Exception:
            print('Unable to connect to server {0} by port {1}'.format(server, port))
            return False
        return True

    def send_query(self, request, recursion_desired=True, debug_mode=False):
        format = DNSMessageFormat()
        query = format.encode(request, recursion_desired, self.ip_version == 6)
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


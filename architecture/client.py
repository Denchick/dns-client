import ipaddress
import socket
import sys


from architecture import request, response

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
        self._connect_server(server, port)

    def _connect_server(self, server, port):
        self.server = server
        self.port = port
        try:
            self.socket.connect((server, port))
        except Exception:
            print('Unable to connect to server {0} by port {1}'.format(server, port))

    def send_query(self, domain_name, recursion_desired=True, type_record='A', debug_mode=False):
        request_object = request.Request(domain_name, recursion_desired, type_record)
        self.socket.send(request_object.get_encoded_request())
        try:
            raw_response = self.socket.recv(1024)
        except Exception:
            print('Timeout: {0}'.format(self.server))
            sys.exit(0)
        response_object = response.Response(raw_response)

        if debug_mode:
            print('Response from {0}'.format(self.server))
            response_object.print()

        if len(response_object.answers) > 0 or not recursion_desired:
            return

        for rr in response_object.additional_RRs:
            if self._connect_server(rr.response_data.ip):
                self.send_query(domain_name, recursion_desired, type_record, debug_mode)


    def disconnect_server(self):
        self.socket.close()
import ipaddress
import socket
import logging

from architecture import request, response

LOGGER_NAME = 'dns-client'
LOGGER = logging.getLogger(LOGGER_NAME)

class DNSClient:
    def __init__(self,
                 server: str,
                 port: int,
                 timeout: int,
                 use_tcp: bool):
        LOGGER.debug('Try to get info from {0} by {1} port using {2} with timeout {3}.'.format(server,
                                                                                          str(port),
                                                                                          'TCP' if use_tcp else 'UDP',
                                                                                          str(timeout)))
        ip_version = ipaddress.ip_address(server).version
        self.ip_version = ip_version
        if ip_version == 4:
            ip_protocol = socket.AF_INET
        elif ip_version == 6:
            ip_protocol = socket.AF_INET6
        else:
            message = "Unknown IP protocol version {0}.".format(ip_version)
            LOGGER.error(message)
            raise AttributeError(message)
        LOGGER.debug("Address {0} is IPv{1}.".format(server, ip_version))
        transport_protocol = socket.SOCK_STREAM if use_tcp else socket.SOCK_DGRAM
        self.socket = socket.socket(ip_protocol, transport_protocol)
        LOGGER.debug("Socket is created.")
        self.socket.settimeout(timeout)
        self._connect_server(server, port)

    def _connect_server(self, server, port):
        self.server = server
        self.port = port
        LOGGER.debug("Let's try connect to the server...")
        try:
            self.socket.connect((server, port))
        except Exception:
            message = 'Unable to connect to server {0} by port {1}.'.format(server, port)
            LOGGER.error(message)
            raise RuntimeError(message)
        LOGGER.debug("It's OK.")

    def send_query(self, domain_name, recursion_desired=True, type_record='A'):
        LOGGER.debug("Try to send query with type '{0}' about {1} with {2}.".format(
            type_record,
            domain_name,
            'recursion desired' if recursion_desired else "no recursion"
        ))
        request_object = request.Request(domain_name, recursion_desired, type_record)
        self.socket.send(request_object.get_encoded_request())
        try:
            raw_response = self.socket.recv(1024)
        except Exception:
            message = 'Timeout: {0}'.format(self.server)
            LOGGER.error(message)
            raise RuntimeError(message)
        response_object = response.Response(raw_response)
        LOGGER.debug("It's OK.")

        LOGGER.info(str(response_object))

        if len(response_object.answers) > 0 or not recursion_desired:
            return

        for rr in response_object.additional_RRs:
            if self._connect_server(rr.response_data.ip):
                self.send_query(domain_name, recursion_desired, type_record)


    def disconnect_server(self):
        LOGGER.debug("Try to disconnect server")
        self.socket.close()
        LOGGER.debug("Disconnected.")
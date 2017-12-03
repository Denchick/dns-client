import struct

from architecture import QUERY_TYPE_NAMES, QUERY_CLASS_NAMES
from architecture.utils import Utils


class DNSQuery:

    def decode(self, message, offset):
        name = Utils.decode_string(message, offset)
        offset = name[0]
        self.name = name[1]
        self.type = Utils.unpack(message[offset:offset + 2])
        self.request_class = Utils.unpack(message[offset + 2: offset + 4])
        return offset + 4

    def set_question(self, name, IPv6):
        self.name = name
        self.type = 28 if IPv6 else 1
        self.request_class = 1

    def encode_domain_name(self):
        name = self.name
        if name.endswith('.'):
            name = name[:-1]
        result = b''
        for domain_name in name.split('.'):
            result += struct.pack('B', len(domain_name))
            result += bytes(domain_name, 'utf-8')
        result += b'\x00'
        return result

    def encode(self):
        result = self.encode_domain_name()
        result += Utils.pack_two_bytes(self.type)
        result += Utils.pack_two_bytes(self.request_class)
        return result

    def print(self):
        ''' for debug mode '''
        print('    Name: {0}'.format(self.name))
        print('    Type: {0}'.format(QUERY_TYPE_NAMES[self.type]))
        print('    Class: {0}'.format(QUERY_CLASS_NAMES[self.request_class]))
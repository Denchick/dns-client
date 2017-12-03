import struct

from architecture import QUERY_TYPE_NAMES, QUERY_CLASS_NAMES
from architecture.utils import Utils

class RecordType:

    def set_type_data(self, message, offset):
        rdata = message[offset:offset + self.rd_lenght]
        if self.type == 1:
            self.type_data = ATypeData(rdata)
        elif self.type == 2:
            self.type_data = NSTypeData(message, offset)
        elif self.type == 5:
            self.type_data = CNAMETypeData(message, offset)
        elif self.type == 15:
            self.type_data = MXTypeData(message, offset)
        elif self.type == 28:
            self.type_data = AAAATypeData(rdata)
        else:
            self.type_data = BinaryTypeData(rdata)

    def decode(self, message, offset):
        name = Utils.decode_string(message, offset)
        offset = name[0]
        self.name = name[1]
        self.type = Utils.unpack(message[offset: offset + 2])
        offset += 2
        self.request_class = Utils.unpack(message[offset: offset + 2])
        offset += 2
        self.ttl = struct.unpack('>I', message[offset:offset + 4])[0]
        offset += 4
        self.rd_lenght = Utils.unpack(message[offset:offset + 2])
        offset += 2
        self.set_type_data(message, offset)
        return offset + self.rd_lenght

    def __str__(self):
        result = []
        result.append('Name: {0}'.format(self.name))
        result.append('Type: {0}'.format(QUERY_TYPE_NAMES[self.type]))
        result.append('Class: {0}'.format(QUERY_CLASS_NAMES[self.request_class]))
        result.append('TTL: {0}'.format(self.ttl))
        return  '\n    '.join(result)

    def print(self):
        '''for debug mode
        '''
        print('    Name: {0}'.format(self.name))
        print('    Type: {0}'.format(QUERY_TYPE_NAMES[self.type]))
        print('    Class: {0}'.format(QUERY_CLASS_NAMES[self.request_class]))
        print('    TTL: {0}'.format(self.ttl))
        self.type_data.print()



class ATypeData:
    def __init__(self, data):
        ip = struct.unpack('BBBB', data)
        self.ip = "{0}.{1}.{2}.{3}".format(ip[0], ip[1], ip[2], ip[3]) # мб просто использовать ip?

    def print(self):
        print('    A: {0}'.format(self.ip))


class AAAATypeData:
    def __init__(self, data):
        self.data = data
        self.ip = ''
        dump = self.hexdump(data)
        for i in range(8):
            value = dump[4*i : 4*i + 4]
            for i in range(4):
                if value[i] != '0':
                    value = value[i:]
                    break
                if i == 3:
                    value = ''
            self.ip += value + ':'
        self.ip = self.ip[:-1]

    def hexdump(self, data):
        result = ''
        for byte in data:
            result += str(hex(256 + byte))[3:]
        return result

    def print(self):
        print('AAAA: {0}'.format(self.ip))

class NSTypeData:
    def __init__(self, message, offset):
        self.name = Utils.decode_string(message, offset)[1]

    def print(self):
        print('NS: {0}'.format(self.name))


class MXTypeData:
    def __init__(self, message, offset):
        self.preference = Utils.unpack(message[offset:offset + 2])
        self.mail_exchanger = Utils.decode_string(message, offset + 4)[1]

    def print(self):
        print('MX: {0} {1}'.format(self.preference, self.mail_exchanger))

class CNAMETypeData:
    def __init__(self, data):
        self.data = data

    def print(self):
        print('Data: {0}'.format(self.data))

class BinaryTypeData:
    def __init__(self, data):
        self.data = data

    def print(self):
        print('Data: {0}'.format(self.data))
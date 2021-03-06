import struct
from architecture.utils import Utils

class ATypeData:
    def __init__(self, data):
        ip = struct.unpack('BBBB', data)
        self.ip = "{0}.{1}.{2}.{3}".format(ip[0], ip[1], ip[2], ip[3]) # мб просто использовать ip?

    def __str__(self):
        return str(self.ip)


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

    @staticmethod
    def hexdump(data):
        result = ''
        for byte in data:
            result += str(hex(256 + byte))[3:]
        return result

    def __str__(self):
        return str(self.ip)


class NSTypeData:
    def __init__(self, message, offset):
        self.name = Utils.decode_string(message, offset)[1]

    def __str__(self):
        return str(self.name)


class BinaryTypeData:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return str(self.data)
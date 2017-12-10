import struct

class Utils:
    def pack_two_bytes(value):
        """ >H means big-endian unsigned short - 2 bytes """
        return struct.pack('>H', value)

    def unpack(data):
        """ >H means big-endian unsigned short - 2 bytes """
        return struct.unpack('>H', data)[0]

    def decode_string(message, offset):
        index = offset
        result = ''
        offset = 0
        while message[index] != 0:
            value = message[index]
            if (value>>6) == 3:
                next = Utils.unpack(message[index:index + 2])
                if offset == 0:
                    offset = index + 2
                index = next ^ (3<<14)
            else:
                index += 1
                result += message[index: index + value].decode('utf-8') + '.'
                index += value
        if offset == 0:
            offset = index + 1
        result = result[:-1]
        return (offset, result)

import struct
import random
import logging

LOGGER_NAME = 'architecture.queries'
LOGGER = logging.getLogger(LOGGER_NAME)

QUERY_TYPE_NAMES = {1 : 'A', 2: 'NS', 5: 'CNAME', 15 : 'MX', 28: 'AAAA'}
OPCODES = { 0 : 'QUERY', 1 : 'IQUERY', 2 : 'STATUS'}
QUERY_CLASS_NAMES = {1  : 'IN'}
message_types = {0 : 'QUERY', 1 : 'RESPONSE'}
RESPONSE_CODE_NAMES = {0 : 'NO ERROR', 1 : 'FORMAT_ERROR', 2 : 'SERVER FAILURE', 3 : 'NAME ERROR', 4 : 'NOT IMPLEMENTED', 5: 'REFUSED'}

def pack(value):
    return struct.pack('>H', value)

def unpack(data):
    return struct.unpack('>H', data)[0]

def decode_string(message, offset):
    index = offset
    result = ''
    offset = 0
    while message[index] != 0:
        value = message[index]
        if (value>>6) == 3:
            next = unpack(message[index:index + 2])
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


class MessageHeader(object):

    def decode(self, message):
        """ decode header """
        self.messageID = unpack(message[0:2])
        meta = unpack(message[2: 4])
        self.rcode = (meta & 15)
        meta >>= 7
        self.ra = (meta & 1)
        meta >>= 1
        self.rd = (meta & 1)
        meta >>= 1
        self.tc = (meta & 1)
        meta >>= 1
        self.aa = (meta & 1)
        meta >>= 1
        self.opcode = (meta & 15)
        meta >>= 4
        self.qr = meta
        self.qd_count = unpack(message[4:6])
        self.an_count = unpack(message[6:8])
        self.ns_count = unpack(message[8:10])
        self.ar_count = unpack(message[10:12])
        return 12

    def generate_ID(self):
        return random.randint(0, 65535)

    def set_question_header(self, recursion_desired):
        """ set header for request """
        self.message_ID = self.generate_ID()
        self.qr = 0
        self.opcode = 0
        self.aa = 0
        self.tc = 0
        self.rd = 1 if recursion_desired else 0
        self.ra = 0
        self.rcode = 0
        self.qd_count = 1
        self.an_count = 0
        self.ns_count = 0
        self.ar_count = 0

    def encode(self):
        result = pack(self.message_ID)
        meta = 0
        meta |= self.qr
        meta <<= 1
        meta |= self.opcode
        meta <<= 4
        meta |= self.aa
        meta <<= 1
        meta |= self.tc
        meta <<= 1
        meta |= self.rd
        meta <<= 1
        meta |= self.ra
        meta <<= 7
        meta |= self.rcode
        result += pack(meta)
        result += pack(self.qd_count)
        result += pack(self.an_count)
        result += pack(self.ns_count)
        result += pack(self.ar_count)
        return result

    def print(self):
        '''for debug mode
        '''
        print('    Message ID: {0}'.format(hex(self.messageID)))
        print('    Query/Responce: {0}'.format(message_types[self.qr]))
        print('    Opcode: {0} ({1})'.format(self.opcode, OPCODES[self.opcode]))
        print('    Authoritative Answer: {0}'.format(bool(self.aa)))
        print('    TrunCation: {0}'.format(bool(self.tc)))
        print('    Recursion Desired: {0}'.format(bool(self.rd)))
        print('    Recursion Available: {0}'.format(bool(self.ra)))
        print('    Responce Code: {0} ({1})'.format(self.rcode, RESPONSE_CODE_NAMES[self.rcode]))
        print('    Questions: {0}'.format(self.qd_count))
        print('    Answers: {0}'.format(self.an_count))
        print('    Authority RRs: {0}'.format(self.ns_count))
        print('    Additional RRs: {0}'.format(self.ar_count))

class DNSQuestion:

    def decode(self, message, offset):
        name = decode_string(message, offset)
        offset = name[0]
        self.name = name[1]
        self.type = unpack(message[offset:offset + 2])
        self.request_class = unpack(message[offset + 2: offset + 4])
        return offset + 4

    def set_question(self, name, IPv6):
        self.name = name
        self.type = 28 if IPv6 else 1
        self.request_class = 1

    def encode_name(self):
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
        result = self.encode_name()
        result += pack(self.type)
        result += pack(self.request_class)
        return result

    def print(self):
        ''' for debug mode '''
        print('    Name: {0}'.format(self.name))
        print('    Type: {0}'.format(QUERY_TYPE_NAMES[self.type]))
        print('    Class: {0}'.format(QUERY_CLASS_NAMES[self.request_class]))


class AResourceData:
    def __init__(self, data):
        ip = struct.unpack('BBBB', data)
        self.ip = "{0}.{1}.{2}.{3}".format(ip[0], ip[1], ip[2], ip[3]) # мб просто использовать ip?

    def print(self):
        print('    A: {0}'.format(self.ip))

class AAAAResourceData:
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
        print('    AAAA: {0}'.format(self.ip))

class NSResourceData:
    def __init__(self, message, offset):
        self.name = decode_string(message, offset)[1]

    def print(self):
        print('    NS: {0}'.format(self.name))

class MXResourceData:
    def __init__(self, message, offset):
        self.preference = unpack(message[offset:offset + 2])
        offset += 2
        self.mail_exchanger = decode_string(message, offset)[1]

    def print(self):
        print('    MX: {0} {1}'.format(self.preference, self.mail_exchanger))

class CNAMEResourceData:
    def __init__(self, data):
        self.data = data

    def print(self):
        print('    Data: {0}'.format(self.data))

class BinaryResourceData:
    def __init__(self, data):
        self.data = data

    def print(self):
        print('    Data: {0}'.format(self.data))

class ResourceRecord:

    def set_resource_data(self, message, offset):
        rdata = message[offset:offset + self.rd_lenght]
        if self.type == 1:
            self.resource_data = AResourceData(rdata)
        elif self.type == 2:
            self.resource_data = NSResourceData(message, offset)
        elif self.type == 5:
            self.resource_data = CNAMEResourceData(message, offset)
        elif self.type == 15:
            self.resource_data = MXResourceData(message, offset)
        elif self.type == 28:
            self.resource_data = AAAAResourceData(rdata)
        else:
            self.resource_data = BinaryResourceData(rdata)

    def decode(self, message, offset):
        name = decode_string(message, offset)
        offset = name[0]
        self.name = name[1]
        self.type = unpack(message[offset: offset + 2])
        offset += 2
        self.request_class = unpack(message[offset: offset + 2])
        offset += 2
        self.ttl = struct.unpack('>I', message[offset:offset + 4])[0]
        offset += 4
        self.rd_lenght = unpack(message[offset:offset + 2])
        offset += 2
        self.set_resource_data(message, offset)
        return offset + self.rd_lenght

    def print(self):
        '''for debug mode
        '''
        print('    Name: {0}'.format(self.name))
        print('    Type: {0}'.format(QUERY_TYPE_NAMES[self.type]))
        print('    Class: {0}'.format(QUERY_CLASS_NAMES[self.request_class]))
        print('    TTL: {0}'.format(self.ttl))
        self.resource_data.print()

class DNSMessageFormat:

    def encode(self, host_name, recursion_desired, IPv6):

        message = b''
        self.header = MessageHeader()
        self.header.set_question_header(recursion_desired)
        message += self.header.encode()
        self.question = DNSQuestion()
        self.question.set_question(host_name, IPv6)
        message += self.question.encode()
        return message

    def decode(self, message):
        self.header = MessageHeader()
        offset = self.header.decode(message)
        self.questions =[]
        self.answers = []
        self.authority_RRs = []
        self.additional_RRs = []
        for i in range(self.header.qd_count):
            self.questions.append(DNSQuestion())
            offset = self.questions[i].decode(message, offset)
        for i in range(self.header.an_count):
            self.answers.append(ResourceRecord())
            offset = self.answers[i].decode(message, offset)
        for i in range(self.header.ns_count):
            self.authority_RRs.append(ResourceRecord())
            offset = self.authority_RRs[i].decode(message, offset)
        for i in range(self.header.ar_count):
            self.additional_RRs.append(ResourceRecord())
            offset = self.additional_RRs[i].decode(message, offset)

    def print(self):
        '''for debug mode
        '''
        print('MESSAGE HEADER')
        self.header.print()
        for i in range(self.header.qd_count):
            print('QUESTION[{0}]'.format(i))
            self.questions[i].print()
        for i in range(self.header.an_count):
            print('ANSWER[{0}]'.format(i))
            self.answers[i].print()
        for i in range(self.header.ns_count):
            print('AUTHORITY_RR[{0}]'.format(i))
            self.authority_RRs[i].print()
        for i in range(self.header.ar_count):
            print('ADDITIONAL_RR[{0}]'.format(i))
            self.additional_RRs[i].print()

    def print_result(self):
        '''output application result
        '''
        for answer in self.answers:
            if answer.type == 1 or answer.type == 28:
                print(answer.resource_data.ip)
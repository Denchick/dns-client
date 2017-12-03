import random

from architecture import OPCODES, MESSAGE_TYPES, RESPONSE_CODE_NAMES
from architecture.utils import Utils


class DNSHeader(object):

    def decode(self, message):
        """ decode header """
        self.messageID = Utils.unpack(message[0:2])
        meta = Utils.unpack(message[2: 4])
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
        self.qd_count = Utils.unpack(message[4:6])
        self.an_count = Utils.unpack(message[6:8])
        self.ns_count = Utils.unpack(message[8:10])
        self.ar_count = Utils.unpack(message[10:12])
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
        result = Utils.pack_two_bytes(self.message_ID)
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
        result += Utils.pack_two_bytes(meta)
        result += Utils.pack_two_bytes(self.qd_count)
        result += Utils.pack_two_bytes(self.an_count)
        result += Utils.pack_two_bytes(self.ns_count)
        result += Utils.pack_two_bytes(self.ar_count)
        return result

    def print(self):
        '''for debug mode
        '''
        print('    Message ID: {0}'.format(hex(self.messageID)))
        print('    Query/Responce: {0}'.format(MESSAGE_TYPES[self.qr]))
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
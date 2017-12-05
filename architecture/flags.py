# https://github.com/rthalley/dnspython/blob/master/dns/flags.py
# https://habrahabr.ru/sandbox/112582/


from architecture import MESSAGE_TYPES, OPCODES, RESPONSE_CODE_NAMES, AUTHORITATIVE, TRUNCATED, RECURSION_DESIRED, \
    RECURSION_AVAILABLE, ANSWER_AUTHENTICATED, NON_AUTHENTICATED_DATA
from architecture.utils import Utils




#: Query Response
QR = 0x8000
#: Opcode
OPCODE = 0x7800
#: Authoritative Answer
AA = 0x0400
#: Truncated Response
TC = 0x0200
#: Recursion Desired
RD = 0x0100
#: Recursion Available
RA = 0x0080
#: Authentic Data
AD = 0x0020
#: Checking Disabled
CD = 0x0010
#: Request Success
RCODE = 0x000F


class Flags:

    def encode(self, recursion_desired=False):
        self._encoded_flags = 0x0000
        if recursion_desired:
            self._encoded_flags |= RD
        return self._encoded_flags

    def decode(self, data: bytes):
        self._encoded_flags = Utils.unpack(data)
        self._decoded_flags = {'qr': (self._encoded_flags & QR) >> 15,
                 'opcode': (self._encoded_flags & OPCODE) >> 14,
                 'aa': (self._encoded_flags & AA) >> 10,
                 'tc': (self._encoded_flags & TC) >> 9,
                 'rd': (self._encoded_flags & RD) >> 8,
                 'ra': (self._encoded_flags & RA) >> 7,
                 'ad': (self._encoded_flags & AD) >> 5,
                 'cd': (self._encoded_flags & CD) >> 4,
                 'rcode': (self._encoded_flags & RCODE)}
        return self._encoded_flags

    def get_QR(self):
        """ Query Response """
        return self._decoded_flags['qr']
    def get_OPCODE(self):
        """ Opcode """
        return self._decoded_flags['opcode']
    def get_AA(self):
        """ Authoritative Answer """
        return self._decoded_flags['aa']

    def get_TC(self):
        """ Truncated Response """
        return self._decoded_flags['tc']

    def get_RD(self):
        """ Recursion Desired """
        return self._decoded_flags['rd']

    def get_RA(self):
        """ Recursion Available """
        return self._decoded_flags['ra']

    def get_AD(self):
        """ Authentic Data """
        return self._decoded_flags['ad']

    def get_CD(self):
        """ Checking Disabled """
        return self._decoded_flags['cd']

    def get_RCODE(self):
        """ Request Success """
        return self._decoded_flags['rcode']

    def print(self):
        print('    Flags: 0x{0:x} ({0:08b})'.format(self._encoded_flags))
        print('        Response: message is {0} ({1})'.format(MESSAGE_TYPES[self.get_QR()], self.get_QR()))
        print('        Opcode: {0} ({1})'.format(OPCODES[self.get_OPCODE()], self.get_OPCODE()))
        print('        Authorative: {0} ({1})'.format(AUTHORITATIVE[self.get_AA()], self.get_AA()))
        print('        Truncated: {0} ({1})'.format(TRUNCATED[self.get_TC()], self.get_TC()))
        print('        Recursion Desired: {0} ({1})'.format(RECURSION_DESIRED[self.get_RD()], self.get_RD()))
        print('        Recursion Available: {0} ({1})'.format(RECURSION_AVAILABLE[self.get_RA()], self.get_RA()))
        print('        Answer authenticated: {0} ({1})'.format(ANSWER_AUTHENTICATED[self.get_AD()], self.get_AD()))
        print('        Non-authenticated data: {0} ({1})'.format(NON_AUTHENTICATED_DATA[self.get_CD()], self.get_CD()))
        print('        Reply code: {0} ({1})'.format(RESPONSE_CODE_NAMES[self.get_RCODE()], self.get_RCODE()))

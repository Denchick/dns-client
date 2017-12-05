import random

from architecture import OPCODES, MESSAGE_TYPES, RESPONSE_CODE_NAMES
from architecture.flags import Flags
from architecture.utils import Utils


class DNSHeader(object):
    def decode(self, message):
        """ decode header """
        self.transaction_id = Utils.unpack(message[0:2])
        self.flags = Flags()
        self.flags.decode(message[2:4])
        self.number_of_questions = Utils.unpack(message[4:6])
        self.number_of_answers = Utils.unpack(message[6:8])
        self.number_of_authority_rrs = Utils.unpack(message[8:10])
        self.number_of_additional_rrs = Utils.unpack(message[10:12])
        return 12

    def generate_ID(self):
        return random.randint(0, 65535)

    def set_question_header(self, recursion_desired=False):
        """ set header for request """
        self.transaction_id = self.generate_ID()
        self.flags = Flags().encode(recursion_desired)
        self.number_of_questions = 1
        self.number_of_answers = 0
        self.number_of_authority_rrs = 0
        self.number_of_additional_rrs = 0

    def encode(self):
        result = Utils.pack_two_bytes(self.transaction_id)
        result += Utils.pack_two_bytes(self.flags)
        result += Utils.pack_two_bytes(self.number_of_questions)
        result += Utils.pack_two_bytes(self.number_of_answers)
        result += Utils.pack_two_bytes(self.number_of_authority_rrs)
        result += Utils.pack_two_bytes(self.number_of_additional_rrs)
        return result

    def print(self):
        '''for debug mode
        '''
        print('    Transaction ID: {0}'.format(hex(self.transaction_id)))
        self.flags.print()
        print('    Questions: {0}'.format(self.number_of_questions))
        print('    Answers: {0}'.format(self.number_of_answers))
        print('    Authority RRs: {0}'.format(self.number_of_authority_rrs))
        print('    Additional RRs: {0}'.format(self.number_of_additional_rrs))
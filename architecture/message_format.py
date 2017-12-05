import struct
import random
import logging

from architecture import NUMBER_BY_QUERY_TYPE_NAMES
from architecture.header import DNSHeader
from architecture.query import DNSQuery
from architecture.record_types import DNSRecordType

LOGGER_NAME = 'architecture.message_format'
LOGGER = logging.getLogger(LOGGER_NAME)

class DNSMessageFormat:

    def __init__(self, type_record=None):
        if type_record is None:
            self.type_record = 1
        try:
            self.type_record = NUMBER_BY_QUERY_TYPE_NAMES[type_record]
        except KeyError:
            raise AttributeError("Unknown type record: {0}".format(type_record))

    def encode(self, host_name, recursion_desired=True):
        message = b''
        self.header = DNSHeader()
        self.header.set_question_header(recursion_desired)
        message += self.header.encode()
        self.question = DNSQuery()
        self.question.set_question(host_name, self.type_record)
        message += self.question.encode()
        return message

    def decode(self, message):
        self.header = DNSHeader()
        offset = self.header.decode(message)
        self.questions =[]
        self.answers = []
        self.authority_RRs = []
        self.additional_RRs = []
        for i in range(self.header.number_of_questions):
            self.questions.append(DNSQuery())
            offset = self.questions[i].decode(message, offset)
        for i in range(self.header.number_of_answers):
            self.answers.append(DNSRecordType())
            offset = self.answers[i].decode(message, offset)
        for i in range(self.header.number_of_authority_rrs):
            self.authority_RRs.append(DNSRecordType())
            offset = self.authority_RRs[i].decode(message, offset)
        for i in range(self.header.number_of_additional_rrs):
            self.additional_RRs.append(DNSRecordType())
            offset = self.additional_RRs[i].decode(message, offset)

    def print(self):
        '''for debug mode
        '''
        self.header.print()
        for i in range(self.header.number_of_questions):
            print('QUESTION[{0}]'.format(i))
            self.questions[i].print()
        for i in range(self.header.number_of_answers):
            print('ANSWER[{0}]'.format(i))
            self.answers[i].print()
        for i in range(self.header.number_of_authority_rrs):
            print('AUTHORITY_RR[{0}]'.format(i))
            print(self.authority_RRs[i])
        for i in range(self.header.number_of_additional_rrs):
            print('ADDITIONAL_RR[{0}]'.format(i))
            print(self.additional_RRs[i])
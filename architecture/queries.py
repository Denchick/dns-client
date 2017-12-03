import struct
import random
import logging

from architecture.dns_header import DNSHeader
from architecture.dns_query import DNSQuery
from architecture.dns_type_records import RecordType

LOGGER_NAME = 'architecture.queries'
LOGGER = logging.getLogger(LOGGER_NAME)

class DNSMessageFormat:

    def encode(self, host_name, recursion_desired, IPv6):

        message = b''
        self.header = DNSHeader()
        self.header.set_question_header(recursion_desired)
        message += self.header.encode()
        self.question = DNSQuery()
        self.question.set_question(host_name, IPv6)
        message += self.question.encode()
        return message

    def decode(self, message):
        self.header = DNSHeader()
        offset = self.header.decode(message)
        self.questions =[]
        self.answers = []
        self.authority_RRs = []
        self.additional_RRs = []
        for i in range(self.header.qd_count):
            self.questions.append(DNSQuery())
            offset = self.questions[i].decode(message, offset)
        for i in range(self.header.an_count):
            self.answers.append(RecordType())
            offset = self.answers[i].decode(message, offset)
        for i in range(self.header.ns_count):
            self.authority_RRs.append(RecordType())
            offset = self.authority_RRs[i].decode(message, offset)
        for i in range(self.header.ar_count):
            self.additional_RRs.append(RecordType())
            offset = self.additional_RRs[i].decode(message, offset)

    def print(self):
        '''for debug mode
        '''
        self.header.print()
        for i in range(self.header.qd_count):
            print('QUESTION[{0}]'.format(i))
            self.questions[i].print()
        for i in range(self.header.an_count):
            print('ANSWER[{0}]'.format(i))
            self.answers[i].print()
        for i in range(self.header.ns_count):
            print('AUTHORITY_RR[{0}]'.format(i))
            print(self.authority_RRs[i])
        for i in range(self.header.ar_count):
            print('ADDITIONAL_RR[{0}]'.format(i))
            print(self.additional_RRs[i])

    def print_result(self):
        '''output application result
        '''
        for answer in self.answers:
            if answer.type == 1 or answer.type == 28:
                print(answer.resource_data.ip)
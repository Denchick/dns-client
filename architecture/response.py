import struct

from architecture import BY_NUMBER_QUERY_TYPE_NAMES, QUERY_CLASS_NAMES
from architecture.flags import Flags
from architecture.record_types import ATypeData, NSTypeData, CNAMETypeData, MXTypeData, AAAATypeData, BinaryTypeData
from architecture.utils import Utils
import logging

LOGGER_NAME = 'dns-client'
LOGGER = logging.getLogger(LOGGER_NAME)

class Response:
    def __init__(self, raw_message):
        LOGGER.debug("Try to parse raw response: {0}".format(raw_message))
        self.header = ResponseHeader(raw_message)
        offset = self.header.get_offfset()
        self.questions =[]
        self.answers = []
        self.authority_RRs = []
        self.additional_RRs = []
        LOGGER.debug("Try to parse a body of raw message")
        for i in range(self.header.number_of_questions):
            self.questions.append(ResponseQuery(raw_message, offset))
            offset = self.questions[i].get_offset()
        for i in range(self.header.number_of_answers):
            self.answers.append(ResponseRecordType(raw_message, offset))
            offset = self.answers[i].get_offset()
        for i in range(self.header.number_of_authority_rrs):
            self.authority_RRs.append(ResponseRecordType(raw_message, offset))
            offset = self.authority_RRs[i].get_offset()
        for i in range(self.header.number_of_additional_rrs):
            self.additional_RRs.append(ResponseRecordType(raw_message, offset))
            offset = self.additional_RRs[i].get_offset()
        LOGGER.debug("Parsed")

    def __str__(self):
        result = str(self.header) + "\n"
        for i in range(self.header.number_of_questions):
            result += 'QUESTION[{0}]\n{1}'.format(i, str(self.questions[i]))
        for i in range(self.header.number_of_answers):
            result += 'ANSWER[{0}]\n{1}'.format(i, str(self.answers[i]))
        for i in range(self.header.number_of_authority_rrs):
            result += 'AUTHORITY_RR[{0}]\n{1}'.format(i, str(self.authority_RRs[i]))
        for i in range(self.header.number_of_additional_rrs):
            result += 'ADDITIONAL_RR[{0}]\n{1}'.format(i, str(self.additional_RRs[i]))
        return result

class ResponseQuery:
    def __init__(self, raw_message, offset):
        raw_domain_name = Utils.decode_string(raw_message, offset)
        self._current_offset = raw_domain_name[0]
        self._domain_name = raw_domain_name[1]
        self._type = Utils.unpack(raw_message[self._current_offset:self._current_offset + 2])
        self._request_class = Utils.unpack(raw_message[self._current_offset + 2: self._current_offset + 4])
        self._current_offset += 4

    def get_offset(self):
        return self._current_offset

    def __str__(self):
        return "    Name: {0}\n    Type: {1}\n    Class: {2}\n".format(
            self._domain_name,
            BY_NUMBER_QUERY_TYPE_NAMES[self._type],
            QUERY_CLASS_NAMES[self._request_class])

class ResponseHeader:
    def __init__(self, raw_message):
        LOGGER.debug("Try to parse raw header: {0}".format(raw_message[0:12]))
        self.transaction_id = Utils.unpack(raw_message[0:2])
        self.flags = Flags()
        self.flags.decode(raw_message[2:4])
        self.number_of_questions = Utils.unpack(raw_message[4:6])
        self.number_of_answers = Utils.unpack(raw_message[6:8])
        self.number_of_authority_rrs = Utils.unpack(raw_message[8:10])
        self.number_of_additional_rrs = Utils.unpack(raw_message[10:12])
        LOGGER.debug("OK.")


    def get_offfset(self):
        return 12

    def __str__(self):
        result = '    Transaction ID: {0}\n'.format(hex(self.transaction_id))
        result += str(self.flags)
        result += '    Questions: {0}\n'.format(self.number_of_questions)
        result += '    Answers: {0}\n'.format(self.number_of_answers)
        result += '    Authority RRs: {0}\n'.format(self.number_of_authority_rrs)
        result += '    Additional RRs: {0}\n'.format(self.number_of_additional_rrs)
        return result

class ResponseRecordType:
    def __init__(self, message, offset):
        name = Utils.decode_string(message, offset)
        self._current_offset = name[0]
        self.name = name[1]
        self.type = Utils.unpack(message[self._current_offset: self._current_offset + 2])
        self._current_offset += 2
        self.request_class = Utils.unpack(message[self._current_offset: self._current_offset + 2])
        self._current_offset += 2
        self.ttl = struct.unpack('>I', message[self._current_offset:self._current_offset + 4])[0]
        self._current_offset += 4
        self.rd_lenght = Utils.unpack(message[self._current_offset:self._current_offset + 2])
        self._current_offset += 2
        self._set_type_data(message, self._current_offset)
        self._current_offset += self.rd_lenght

    def _set_type_data(self, message, offset):
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

    def get_offset(self):
        return self._current_offset

    def __str__(self):
        result = '    Name: {0}\n'.format(self.name)
        result += '    Type: {0}\n'.format(BY_NUMBER_QUERY_TYPE_NAMES[self.type])
        result += '    Class: {0}\n'.format(QUERY_CLASS_NAMES[self.request_class])
        result += '    TTL: {0}\n'.format(self.ttl)
        result += str(self.type_data) + "\n"
        return result
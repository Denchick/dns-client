import struct

from architecture import BY_NUMBER_QUERY_TYPE_NAMES, QUERY_CLASS_NAMES, record_types
from architecture.flags import Flags
from architecture.record_types import ATypeData, NSTypeData, CNAMETypeData, MXTypeData, AAAATypeData, \
    BinaryTypeData
from architecture.utils import Utils


class Response:
    def __init__(self, raw_message):
        self.header = ResponseHeader(raw_message)
        offset = self.header.get_offfset()
        self.questions =[]
        self.answers = []
        self.authority_RRs = []
        self.additional_RRs = []
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

    def print(self):
        self.header.print()
        for i in range(self.header.number_of_questions):
            print('QUESTION[{0}]'.format(i))
            self.questions[i].print()
        for i in range(self.header.number_of_answers):
            print('ANSWER[{0}]'.format(i))
            self.answers[i].print()
        for i in range(self.header.number_of_authority_rrs):
            print('AUTHORITY_RR[{0}]'.format(i))
            self.authority_RRs[i].print()
        for i in range(self.header.number_of_additional_rrs):
            print('ADDITIONAL_RR[{0}]'.format(i))
            self.additional_RRs[i].print()

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

    def print(self):
        ''' for debug mode '''
        print('    Name: {0}'.format(self._domain_name))
        print('    Type: {0}'.format(BY_NUMBER_QUERY_TYPE_NAMES[self._type]))
        print('    Class: {0}'.format(QUERY_CLASS_NAMES[self._request_class]))

class ResponseHeader:
    def __init__(self, raw_message):
        self.transaction_id = Utils.unpack(raw_message[0:2])
        self.flags = Flags()
        self.flags.decode(raw_message[2:4])
        self.number_of_questions = Utils.unpack(raw_message[4:6])
        self.number_of_answers = Utils.unpack(raw_message[6:8])
        self.number_of_authority_rrs = Utils.unpack(raw_message[8:10])
        self.number_of_additional_rrs = Utils.unpack(raw_message[10:12])

    def get_offfset(self):
        return 12

    def print(self):
        print('    Transaction ID: {0}'.format(hex(self.transaction_id)))
        self.flags.print()
        print('    Questions: {0}'.format(self.number_of_questions))
        print('    Answers: {0}'.format(self.number_of_answers))
        print('    Authority RRs: {0}'.format(self.number_of_authority_rrs))
        print('    Additional RRs: {0}'.format(self.number_of_additional_rrs))

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

    def print(self):
        '''for debug mode
        '''
        print('    Name: {0}'.format(self.name))
        print('    Type: {0}'.format(BY_NUMBER_QUERY_TYPE_NAMES[self.type]))
        print('    Class: {0}'.format(QUERY_CLASS_NAMES[self.request_class]))
        print('    TTL: {0}'.format(self.ttl))
        self.type_data.print()
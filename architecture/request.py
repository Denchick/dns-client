import random
import struct

from architecture import NUMBER_BY_QUERY_TYPE_NAMES
from architecture.flags import Flags
from architecture.utils import Utils


class Request:

    def __init__(self, domain_name, recursion_desired=True, type_record=None):
        if type_record is None:
            self.type_record = 1
        try:
            self.type_record = NUMBER_BY_QUERY_TYPE_NAMES[type_record]
        except KeyError:
            raise AttributeError("Unknown type record: {0}".format(type_record))
        self.domain_name = domain_name
        self.recursion_desired = recursion_desired
        self.request_class = 1
        self._message = self._encode()

    def _encode(self):
        message = b''
        header = RequestHeader(self.recursion_desired)
        message += header.get_encoded_header()
        query = RequestQuery(self.domain_name, self.type_record, self.request_class)
        message += query.get_encoded_question()
        return message

    def get_encoded_request(self):
        return self._message

class RequestQuery:
    def __init__(self, domain_name, type_record, request_class):
        self.domain_name = domain_name
        self.type_record = type_record
        self.request_class = request_class

    def get_encoded_question(self):
        result = self._get_encoded_domain_name()
        result += Utils.pack_two_bytes(self.type_record)
        result += Utils.pack_two_bytes(self.request_class)
        return result

    def _get_encoded_domain_name(self):
        name = self.domain_name
        if name.endswith('.'):
            name = name[:-1]
        result = b''
        for domain_name_part in name.split('.'):
            result += struct.pack('B', len(domain_name_part))
            result += bytes(domain_name_part, 'utf-8')
        result += b'\x00'
        return result

class RequestHeader:
    def __init__(self, recursion_desired=False):
        self.transaction_id = self._generate_ID()
        self.flags = Flags().encode(recursion_desired)
        self.number_of_questions = 1
        self.number_of_answers = 0
        self.number_of_authority_rrs = 0
        self.number_of_additional_rrs = 0
        self._raw_data = self._encode()

    def _generate_ID(self):
        return random.randint(0, 65535)

    def get_encoded_header(self):
        return self._raw_data

    def _encode(self):
        result = Utils.pack_two_bytes(self.transaction_id)
        result += Utils.pack_two_bytes(self.flags)
        result += Utils.pack_two_bytes(self.number_of_questions)
        result += Utils.pack_two_bytes(self.number_of_answers)
        result += Utils.pack_two_bytes(self.number_of_authority_rrs)
        result += Utils.pack_two_bytes(self.number_of_additional_rrs)
        return result
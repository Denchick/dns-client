import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from architecture.response import ResponseQuery, ResponseRecordType
from architecture.response import ResponseHeader


class TestResponse(unittest.TestCase):

    def setUp(self):
        self.raw_message = b"\x8f\xd4\x81\x80\x00\x01\x00\x05\x00\x00\x00\x00\x04mail\x06yandex\x02ru\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\xbc\x00\x04\xd5\xb4\xc1}\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\xbc\x00\x04\xd5\xb4\xcc}\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\xbc\x00\x04W\xfa\xfb}\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\xbc\x00\x04W\xfa\xfa}\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\xbc\x00\x04]\x9e\x86}"
        self.raw_message2 = b'\xbd\x17\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00\x04mail\x06yandex\x02ru\x00\x00\x1c\x00\x01\xc0\x0c\x00\x1c\x00\x01\x00\x00\x00\xd8\x00\x10*\x02\x06\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00%'

    def test_response_init(self):
        query = ResponseQuery(self.raw_message, 12)
        self.assertEqual(query._current_offset, 32)
        self.assertEqual(query._domain_name, 'mail.yandex.ru')
        self.assertEqual(query._type, 1)
        self.assertEqual(query._request_class, 1)

    def test_responseHeader(self):
        header = ResponseHeader(self.raw_message)
        self.assertEqual(header.transaction_id, 36820)
        self.assertEqual(header.flags._encoded_flags, 0x8180)
        self.assertEqual(header.number_of_questions, 1)
        self.assertEqual(header.number_of_authority_rrs, 0)
        self.assertEqual(header.number_of_answers, 5)
        self.assertEqual(header.number_of_additional_rrs, 0)

    def test_responseQuery(self):
        query = ResponseQuery(self.raw_message, 12)
        self.assertEqual(query._current_offset, 32)
        self.assertEqual(query._domain_name, 'mail.yandex.ru')
        self.assertEqual(query._request_class, 1)
        self.assertEqual(query._type, 1)
        expected = "    Name: mail.yandex.ru\n    Type: A\n    Class: IN\n"
        self.assertEqual(str(query), expected)
        self.assertEqual(query.get_offset(), 32)

    def test_ResponseRecordType(self):
        record = ResponseRecordType(self.raw_message2, 32)
        self.assertEqual(record.name, 'mail.yandex.ru')
        self.assertEqual(record.type, 28)
        self.assertEqual(record.request_class, 1)
        self.assertEqual(record.ttl, 216)
        self.assertEqual(record.get_offset(), 60)
        self.assertEqual(str(record), str(record))

if __name__ == "__main__":
    unittest.main()
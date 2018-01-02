import unittest

from architecture.response import ResponseQuery, ResponseHeader


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.raw_message = b"\x8f\xd4\x81\x80\x00\x01\x00\x05\x00\x00\x00\x00\x04mail\x06yandex\x02ru\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\xbc\x00\x04\xd5\xb4\xc1}\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\xbc\x00\x04\xd5\xb4\xcc}\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\xbc\x00\x04W\xfa\xfb}\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\xbc\x00\x04W\xfa\xfa}\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\xbc\x00\x04]\x9e\x86}"

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
        header = ResponseHeader(self.raw_message)
        self.assertEqual(header.transaction_id, 36820)
        self.assertEqual(header.flags._encoded_flags, 0x8180)
        self.assertEqual(header.number_of_questions, 1)
        self.assertEqual(header.number_of_authority_rrs, 0)
        self.assertEqual(header.number_of_answers, 5)
        self.assertEqual(header.number_of_additional_rrs, 0)
        self.assertEqual(header.get_offfset(), 12)
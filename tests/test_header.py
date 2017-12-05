import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from architecture import header


class TestHeader(unittest.TestCase):

    def setUp(self):
        self.header1 = header.DNSHeader()

    def test_generate_ID_shouldReturnIntegerFromZeroTo65536(self):
        for i in range(65536):
            self.assertTrue(0 <= self.header1.generate_ID() < 65536)

    def test_correctEncodingHeader_whenRecursionNotDesired(self):
        self.header1.set_question_header(recursion_desired=False)
        actual = self.header1.encode()

        expected_flags = b'\x00\x00'
        expected_qd_count = b'\x00\x01'
        expected_an_count = b'\x00\x00'
        expected_ns_count = b'\x00\x00'
        expected_ar_count = b'\x00\x00'

        self.assertTrue(len(actual) == 12)
        self.assertEqual(expected_flags, actual[2:4])
        self.assertEqual(actual[4:6], expected_qd_count)
        self.assertEqual(actual[6:8], expected_an_count)
        self.assertEqual(actual[8:10], expected_ns_count)
        self.assertEqual(actual[10:12], expected_ar_count)

    def test_correctEncodingHeader_whenRecursionDesired(self):
        self.header1.set_question_header(recursion_desired=True)
        actual = self.header1.encode()

        expected_flags = b'\x01\x00'
        expected_qd_count = b'\x00\x01'
        expected_an_count = b'\x00\x00'
        expected_ns_count = b'\x00\x00'
        expected_ar_count = b'\x00\x00'

        self.assertTrue(len(actual) == 12)
        self.assertEqual(expected_flags, actual[2:4])
        self.assertEqual(actual[4:6], expected_qd_count)
        self.assertEqual(actual[6:8], expected_an_count)
        self.assertEqual(actual[8:10], expected_ns_count)
        self.assertEqual(actual[10:12], expected_ar_count)

    def test_correctHeaderDecoding(self):
        data = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b'
        self.header1.decode(data)
        self.assertEqual(1, self.header1.transaction_id)
        self.assertEqual(2, self.header1.qr)
        self.assertEqual(3, self.header1.opcode)
        self.assertEqual(4, self.header1.tc)
        self.assertEqual(5, self.header1.rd)
        self.assertEqual(6, self.header1.number_of_questions)
        self.assertEqual(7, self.header1.number_of_answers)
        self.assertEqual(8, self.header1.number_of_authority_rrs)
        self.assertEqual(9, self.header1.number_of_additional_rrs)

if __name__ == "__main__":
    unittest.main()
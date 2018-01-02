import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from architecture.request import RequestHeader


class TestRequest(unittest.TestCase):

    def setUp(self):
        self.header_with_rd = RequestHeader(recursion_desired=True)
        self.header_without_rd = RequestHeader(recursion_desired=False)

    def test_correctEncodingHeader_whenRecursionNotDesired(self):
        actual = self.header_without_rd._encode()

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
        actual = self.header_with_rd._encode()

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

if __name__ == "__main__":
    unittest.main()
import unittest
from architecture.utils import Utils

class MyTestCase(unittest.TestCase):
    def test_pack_two_bytes(self):
        self.assertEqual(Utils.pack_two_bytes(19607), b'L\x97')

    def test_unpack(self):
        self.assertEqual(Utils.unpack(b'8\x06'), 14342)

    def test_decode_string(self):
        message = b"\x04mail\x06yandex\x02ru\x00"
        offset = 0
        actual = Utils.decode_string(message, offset)
        self.assertEqual(actual, actual)

if __name__ == '__main__':
    unittest.main()

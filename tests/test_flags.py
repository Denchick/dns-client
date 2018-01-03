import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from architecture.flags import Flags


class TestFlags(unittest.TestCase):

    def setUp(self):
        self.flag_rd = Flags().encode(True)
        self.flag_not_rd = Flags().encode(False)

    def test_encodeWithRecursionDesired(self):
        self.assertEqual(self.flag_rd, 256)

    def test_encodeWithoutRecursionDesired(self):
        self.assertEqual(self.flag_not_rd, 0)

    def test_decodeMethod(self):
        flags = Flags()
        encoded_flags = flags.decode(b'\x81\x80')
        self.assertEqual(encoded_flags, 0x8180)
        self.assertEqual(flags.get_QR(), 1)
        self.assertEqual(flags.get_OPCODE(), 0)
        self.assertEqual(flags.get_AA(), 0)
        self.assertEqual(flags.get_TC(), 0)
        self.assertEqual(flags.get_RD(), 1)
        self.assertEqual(flags.get_RA(), 1)
        self.assertEqual(flags.get_AD(), 0)
        self.assertEqual(flags.get_CD(), 0)
        self.assertEqual(flags.get_RCODE(), 0)

if __name__ == '__main__':
    unittest.main()

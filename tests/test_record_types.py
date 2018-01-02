import unittest

from architecture.record_types import ATypeData, AAAATypeData, NSTypeData


class TestsRecordTypes(unittest.TestCase):

    def test_ATypeData(self):
        data = b'\xd5\xb4\xc1}'
        record = ATypeData(data)
        self.assertEqual(record.ip, '213.180.193.125')
        self.assertEqual(str(record), '213.180.193.125')

    def test_AAAATypeData(self):
        data = b'*\x02\x06\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00%'
        record = AAAATypeData(data)
        self.assertEqual(record.data, data)
        self.assertEqual(record.ip, '2a02:6b8::::::25')
        self.assertEqual(str(record), '2a02:6b8::::::25')

    def test_AAAATypeData_hexdumpWorksCorrectly(self):
        data = b'*\x02\x06\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00%'
        hexdump = AAAATypeData.hexdump(data)

        self.assertEqual(hexdump, '2a0206b8000000000000000000000025')

    def test_NSTypeData(self):
        message = b'9\x0f\x81\x80\x00\x01\x00\x03\x00\x00\x00\x00\x04mail\x06yandex\x02ru\x00\x00\x02\x00\x01\xc0\x0c\x00\x02\x00\x01\x00\x00T_\x00\x06\x03ns6\xc0\x11\xc0\x0c\x00\x02\x00\x01\x00\x00T_\x00\x06\x03ns3\xc0\x11\xc0\x0c\x00\x02\x00\x01\x00\x00T_\x00\x06\x03ns4\xc0\x11'
        offset = 44

        record = NSTypeData(message, offset)

        self.assertEqual(record.name, 'ns6.yandex.ru')


if __name__ == '__main__':
    unittest.main()

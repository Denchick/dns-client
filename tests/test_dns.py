import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from dns import dns


class TestDns(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_correctIp_whenDomainIsYandexRu(self):
        domain = 'yandex.ru'

        dns_test = dns.DNS()
        response = dns_test.resolve(domain)

        actual = set(response.IP)
        expected = set([    ])
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()

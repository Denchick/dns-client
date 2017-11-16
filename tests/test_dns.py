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

        dns_test = dns.DNS(domain)
        response = dns_test.response
        actual = response.IP
        self.assertEqual('5.255.255.50', actual)


if __name__ == "__main__":
    unittest.main()

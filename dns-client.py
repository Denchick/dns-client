#!/usr/bin/env python3
""" DNS клиент """
from architecture.client import DNSClient

ERROR_EXCEPTION = 1
ERROR_WRONG_SETTINGS = 2
ERROR_PYTHON_VERSION = 3
ERROR_MODULES_MISSING = 4

import sys

if sys.version_info < (3, 0):
    print('Используйте Python версии 3.0 и выше', file=sys.stderr)
    sys.exit(ERROR_PYTHON_VERSION)

import argparse

try:
    from architecture import client
except Exception as e:
    print('Модули не найдены: "{}"'.format(e), file=sys.stderr)
    sys.exit(ERROR_MODULES_MISSING)

__version__ = '0.1'
__author__ = 'Volkov Denis'
__email__ = 'denchick1997@mail.ru'


# -type — тип информации, которую хотим получить, возможные типы: txt, soa, ptr, ns, mx, mr, minfo, mg, mb, hinfo, gid, cname, a, any;
# -port — другой порт DNS сервера;
# -recurse — использоваться другие DNS серверы, если на этом нет ответа;
# -retry — количество попыток получить нужную информацию;
# -timeout — время между попытками запросов к серверу;
# -fail — пробовать другой сервер имен, если этот вернул ошибку.

def create_parser():
    """ Разбор аргументов командной строки """
    parser = argparse.ArgumentParser(description='DNS клиент.')

    parser.add_argument(
        'domain', type=str,
        help='Домен, для которого необходимо узнать IP-адрес.')
    parser.add_argument(
        '-s', '--server', type=str, default='8.8.8.8',
        help='Использовать другой DNS сервер вместо стандартного')
    parser.add_argument(
        '-t', '--type', type=str, default='A',
        help='Тип информации, которую хотим получить, возможные типы: A, NS, AAAA. По умолчанию A - IPv4')
    parser.add_argument(
        '-p', '--port', type=int, default=53,
        help='Порт DNS сервера. По умолчанию 53.')
    parser.add_argument(
        '-r', '--recursion-desired', action='store_true', default=True,
        help='Рекурсивный запрос. Как правила, на этот флаг в запросе сервера не обращают внимания.')
    parser.add_argument(
        '-to', '--timeout', type=int, default=100,
        help='Время между попытками запросов к серверу.')
    parser.add_argument(
        '-tcp', '--usetcp', type=bool, default=False,
        help='Использовать TCP вместо UDP по-умолчанию.'
    )
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help='Режим debug.')
    parser.add_argument(
        '--version', action='store_true', default=False,
        help="Печатает версию утилиты и выходит.")
    return parser.parse_args()


def main():
    args = create_parser()

    if args.version:
        print(__version__)
        sys.exit()

    dns_client = DNSClient(
        args.server,
        args.port,
        args.timeout,
        args.usetcp)
    dns_client.send_query(args.domain, recursion_desired=args.recursion_desired, type_record=args.type, debug_mode=args.debug)
    dns_client.disconnect_server()

if __name__ == "__main__":
    main()

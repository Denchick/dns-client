#!/usr/bin/env python3
""" DNS клиент """
import logging

import colorama
import coloredlogs
import os

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
    from architecture import client, flags, record_types, request, response, server_resolver, utils
except Exception as e:
    print('Модули не найдены: "{}"'.format(e), file=sys.stderr)
    sys.exit(ERROR_MODULES_MISSING)

__version__ = '1.0'
__author__ = 'Volkov Denis'
__email__ = 'denchick1997@mail.ru'

LOGGER_NAME = 'dns-client'
LOGGER = logging.getLogger(LOGGER_NAME)

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
        help='Использовать TCP вместо UDP по-умолчанию.')
    parser.add_argument(
        '-v', '--verbose', action='store_true', default=False,
        help='Вывести информацию на консоль.')
    parser.add_argument(
        '--version', action='store_true', default=False,
        help="Печатает версию утилиты и выходит.")
    return parser.parse_args()

def initialize_logger(is_verbose):
    if 'win' in sys.platform:
        # для корректного отображения цветов в windows
        colorama.init()

    log = logging.StreamHandler() if is_verbose else logging.FileHandler(os.path.join('logs', 'log.log')  , "w")
    formatter = coloredlogs.ColoredFormatter if is_verbose else logging.Formatter
    log.setFormatter(formatter(
        '%(asctime)s [%(levelname)s <%(name)s>] %(message)s'))
    log.setLevel(logging.DEBUG)

    for module in (sys.modules[__name__], client):
        logger = logging.getLogger(module.LOGGER_NAME)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(log)

def main():
    args = create_parser()

    if args.version:
        print(__version__)
        sys.exit()

    initialize_logger(args.verbose)

    LOGGER.debug("Application started.")
    dns_client = DNSClient(args.server,
                           args.port,
                           args.timeout,
                           args.usetcp)
    dns_client.send_query(args.domain,
                          args.recursion_desired,
                          args.type)
    dns_client.disconnect_server()

    LOGGER.debug("Application is end.")

if __name__ == "__main__":
    main()

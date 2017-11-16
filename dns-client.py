#!/usr/bin/env python3
""" DNS клиент """

ERROR_EXCEPTION = 1
ERROR_WRONG_SETTINGS = 2
ERROR_PYTHON_VERSION = 3
ERROR_MODULES_MISSING = 4

import sys

if sys.version_info < (3, 0):
    print('Используйте Python версии 3.0 и выше', file=sys.stderr)
    sys.exit(ERROR_PYTHON_VERSION)

import argparse
import logging

try:
    from dns import *
except Exception as e:
    print('Модули не найдены: "{}"'.format(e), file=sys.stderr)
    sys.exit(ERROR_MODULES_MISSING)

__version__ = '0.1'
__author__ = 'Volkov Denis'
__email__ = 'denchick1997@mail.ru'

LOGGER_NAME = 'dns-client'
LOGGER = logging.getLogger(LOGGER_NAME)


# -type — тип информации, которую хотим получить, возможные типы: txt, soa, ptr, ns, mx, mr, minfo, mg, mb, hinfo, gid, cname, a, any;
# -port — другой порт DNS сервера;
# -recurse — использоваться другие DNS серверы, если на этом нет ответа;
# -retry — количество попыток получить нужную информацию;
# -timeout — время между попытками запросов к серверу;
# -fail — пробовать другой сервер имен, если этот вернул ошибку.

def create_parser():
    """ Разбор аргументов командной строки """
    parser = argparse.ArgumentParser(description="""DNS клиент.""")

    parser.add_argument('domain', type=str,
        help="Домен, для которого необходимо узнать IP-адрес.")
    parser.add_argument('-s', '--server', type=str,
        help="Использовать другой DNS сервер вместо стандартного - ")
    parser.add_argument(
        '-t', '--type', type=str, default='ns',
        help="""Тип информации, которую хотим получить, возможные типы: txt, soa, ptr, ns, mx, 
        mr, minfo, mg, mb, hinfo, gid, cname, a, any""")
    parser.add_argument(
        '-p', '--port', type=int, default=53,
        help='Порт DNS сервера. По умолчанию 53.')
    parser.add_argument(
        '-r', '--recursive', action='store_true', default=False,
        help='Использоваться другие DNS серверы, если на этом нет ответа;')
    parser.add_argument(
        '-r', '--retry', type=int, default=3,
        help='Количество попыток получить нужную информацию.')
    parser.add_argument(
        '-to', '--timeout', type=int, default=100,
        help='Время между попытками запросов к серверу.')
    parser.add_argument(
        '-f', '--fail', action='store_true', default=False, help="""Режим debug. Временные файлы не удаляются. Warning! 
        В этом режиме папку с временными файлами необходимо удалять самостоятельно во избежание падения утилиты.""")
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False, help="""Режим debug. Временные файлы не удаляются. Warning! 
        В этом режиме папку с временными файлами необходимо удалять самостоятельно во избежание падения утилиты.""")
    return parser.parse_args()


def main():
    args = create_parser()

    log = logging.StreamHandler(sys.stderr)
    log.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s <%(name)s>] %(message)s'))

    for module in (sys.modules[__name__], map_reduce):
        logger = logging.getLogger(module.LOGGER_NAME)
        logger.setLevel(logging.DEBUG if args.debug else logging.ERROR)
        logger.addHandler(log)

    LOGGER.info('Application is start.')



if __name__ == "__main__":
    main()

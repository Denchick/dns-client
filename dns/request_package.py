""" Запрос """


class Request:
    """ Просто удобный класс с полями, как в wireshark """
    def __init__(self, domain):
        """ Должен из заданных параметров DNS-запроса формировать строку байт - сообщение DNS серверу """
        if not isinstance(domain, str):
            raise AttributeError("Attribute domain must be a string, but {0} got.".format(type(str)))
        self._domain = domain
        self._transaction_id = '0x0001'
        self._flags = '0x0100'
        self._questions = '0x0001'
        self._answer_RRs = '0x0000'
        self._authority_RRs = '0x0000'
        self._additional_RRs = '0x0000'
        self._queries = self.get_queries()

    def get_queries(self):
        """ Поле Queries имеет следующую структуру. 
        1. Указывается длина имени n-ого уровня(1 байт) - число от 1 до 255
        2. Указывается название уровня
        .......
        2n-1. Указывается длина имени 1-го уровня.
        2n. Указывается название 1-го уровня
        В конец добавляется 0 байт. """
        result = []
        for e in self._domain.split('.'):
            if e == '':
                continue
            result.append(len(e))
            result.append(e)
        result.append('0x00')
        return bytes([int for e in result.split()])

    def __str__(self):
        return """Transaction ID: {0}
        Flags: {1}
        Questions: 1
        Answer RRs: 0
        Authority RRs: 0
        Additional RRs: 0
        Queries:
            Name: {2}
            Type: A (Host Address) (1)
            Class: IN (0x0001)""".format(self._transaction_id, self._flags, self._domain)



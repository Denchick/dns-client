" Ответ "

from . import dns_fields


class Response:
    """ Просто удобный класс с полями, как в wireshark """

    def __init__(self, response:bytes):
        """ Должен из байтовой строки - ответа сервера - получить нормальное представление данных"""
        if not isinstance(response, bytes):
            raise AttributeError("Attribute domain must be a string, but {0} got.".format(type(response)))
        self._response = response
        self._pointer = 0

        self._transaction_id = self.get_next_bytes_from_response(2)
        self._flags = self.get_next_bytes_from_response(2)
        self._questions = self.get_next_bytes_from_response(2)
        self._answer_RRs = self.get_next_bytes_from_response(2)
        self._authority_RRs = self.get_next_bytes_from_response(2)
        self._additional_RRs = self.get_next_bytes_from_response(2)
        self._parse_queries()
        self._parse_answers()

    def get_next_bytes_from_response(self, count:int):
        if self._is_answer_will_be_read(count):
            raise RuntimeError
        result = self._response[self._pointer: self._pointer + count]
        self._pointer += count
        return result

    def _is_answer_was_read(self):
        return self._pointer + 1 >= len(self._response)

    def _is_answer_will_be_read(self, count):
        return self._pointer + ord(count) > len(self._response)

    def _parse_queries(self):
        domain = []
        while True:
            current_levels_length = ord(self.get_next_bytes_from_response(1))
            if current_levels_length == 0:
                break
            domain.append(self.get_next_bytes_from_response(current_levels_length))
        _type = self.get_next_bytes_from_response(2)
        _class = self.get_next_bytes_from_response(2)
        self._queries = dns_fields.Queries(domain, _type, _class)

    def _parse_answers(self):
        self._answers = []
        while True:
            name = self.get_next_bytes_from_response(2)
            type = self.get_next_bytes_from_response(2)
            _class = self.get_next_bytes_from_response(2)
            time_to_live = self.get_next_bytes_from_response(4)
            data_legth = self.get_next_bytes_from_response(1)
            address = self.get_next_bytes_from_response(data_legth)

            answers = dns_fields.Answers(name, type, _class, time_to_live, data_legth, address)
            self._answers.append(answers)

    @property
    def IPs(self):
        return self._answers

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
            Class: IN (0x0001)""".format(self._transaction_id, self._flags, self.domain)

""" Описывает общие поля из request и response """


class Flags:
    pass


class Queries:
    """ Описывает поле Queries """
    def __init__(self, _name, _type, _class):
        self._name = _name
        self._type = _type
        self._class = _class


class Answers:
    """ Описывает поле Answers """
    def __init__(self, _name, _type, _class, _time_to_live, _data_length, _address):
        self._name = _name
        self._type = _type
        self._class = _class
        self._time_to_live = _time_to_live
        self._data_length = _data_length
        self._address = _address

    @property
    def IP(self):
        return self._address

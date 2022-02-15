from dataclasses import fields, dataclass
from datetime import date, datetime
from functools import wraps

from core.trancoder.exceptions import InvalidTrancoderConfigurationException


class TrancodeMeta(type):
    pass


def trancode_object(cls):
    def wrapper(*args, **kwargs):
        for field in fields(cls):
            exec(f'cls.{field.name}.value = kwargs.get("{field.name}")')
        if kwargs.get("trancode"):
            cls.trancode = kwargs.get("trancode")

        return cls

    def to_trancode():
        return "".join([field.default.to_trancode() for field in fields(cls)])

    def from_trancode():
        begin: int = 0
        end: int = 0

        for field in fields(cls):
            end += field.default.size
            field.default.value = field.default.from_trancode(
                cls.trancode[begin:end]
            )
            begin = end

    setattr(cls, "to_trancode", to_trancode)
    setattr(cls, "from_trancode", from_trancode)

    return wrapper


@dataclass
class TrancodeField:
    name: str
    size: int
    field_type: type
    precision: int = 0
    date_format: str = ""
    value: object = None
    to_trancode = None
    from_trancode = None

    def __post_init__(self):
        if self.field_type == str:
            self.to_trancode = self._from_str
            self.from_trancode = self._to_str
        elif self.field_type == int:
            self.to_trancode = self._from_int
            self.from_trancode = self._to_int
        elif self.field_type == float:
            self.to_trancode = self._from_float
            self.from_trancode = self._to_float
        elif self.field_type == date or self.field_type == datetime:
            self.to_trancode = self._from_date
            self.from_trancode = self._to_date
        else:
            self.to_trancode = self.value
            self.from_trancode = self.value

    def _from_str(self):
        return self.value.ljust(self.size)

    def _from_int(self, value=None):
        value = value if value else self.value
        return str(int(value)).rjust(self.size, "0")

    def _from_float(self):
        if self.precision:
            value = self.value
            value *= pow(10, self.precision)
            return self._from_int(value)
        else:
            raise InvalidTrancoderConfigurationException(
                'Para campos de valor, é necessário informar o parâmetro "precision"'
            )

    def _from_date(self):
        if self.date_format:
            return self.value.strftime(self.date_format)
        else:
            raise InvalidTrancoderConfigurationException(
                'Para campos de data, é necessário informar o parâmetro "date_format"'
            )

    @staticmethod
    def _to_str(trancode: str):
        return trancode.strip()

    @staticmethod
    def _to_int(trancode: str):
        return int(trancode)

    def _to_float(self, trancode: str):
        return self._to_int(trancode) / pow(10, self.precision)

    def _to_date(self, trancode: str):
        return datetime.strptime(trancode, self.date_format)


def isstr(value: object):
    return isinstance(value, str)


def isint(value: object):
    return isinstance(value, int)


def isfloat(value: object):
    return isinstance(value, float)


def isdate(value: object):
    return isinstance(value, date) or isinstance(value, datetime)

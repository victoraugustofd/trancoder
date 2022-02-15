from dataclasses import dataclass
from datetime import date

from core.trancoder.trancoder import (
    trancode_object,
    TrancodeMeta,
    TrancodeField,
)


class Teste:
    def __init__(self, a):
        self.a = a

    # @trancode_field(name="teste", field_type=str, size=1)
    def get_a(self):
        return self.a


@trancode_object
@dataclass
class Teste2(metaclass=TrancodeMeta):
    campo1: TrancodeField = TrancodeField(
        name="a_field", size=23, field_type=int
    )
    campo2: TrancodeField = TrancodeField(
        name="b_field", size=19, field_type=str
    )
    campo3: TrancodeField = TrancodeField(
        name="b_field", size=17, field_type=float, precision=2
    )
    campo4: TrancodeField = TrancodeField(
        name="b_field", size=14, field_type=date, date_format="%Y%m%d%H%M%S"
    )

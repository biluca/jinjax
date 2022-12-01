from const import KEYWORDS_LIST


class Nominal:
    def __init__(self, type, value=None, position_start=None, position_end=None):
        self.type = type
        self.value = value

        if position_start:
            self.position_start = position_start.copy()
            self.position_end = position_start.copy()
            self.position_end.advance()

        if position_end:
            self.position_end = position_end.copy()

    def __repr__(self) -> str:
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"

    def is_keyword(self):
        return self.type in KEYWORDS_LIST

    def is_from_type(self, type):
        return self.type == type

    def is_from_types(self, types):
        return self.type in types

    def matches(self, value):
        return self.value == value

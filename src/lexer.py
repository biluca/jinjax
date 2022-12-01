from const import *
from errors import *
from position import Position
from nominal import Nominal

class Lexer:
    def __init__(self, file_name, text):
        self.file_name = file_name
        self.text = text
        self.position = Position(-1, 0, -1, file_name, text)
        self.current_char = None
        self.advance()

    def __repr__(self) -> str:
        pass

    def advance(self):
        self.position.advance(self.current_char)
        if self.position.index < len(self.text):
            self.current_char = self.text[self.position.index]
        else:
            self.current_char = None

    def make_number(self):
        num_str = ""
        dot_count = 0
        position_start = self.position.copy()

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Nominal(NOMINAL_TYPE_INTEGER, int(num_str), position_start, self.position)
        else:
            return Nominal(NOMINAL_TYPE_FLOAT, float(num_str), position_start, self.position)
    
    def make_identifier_or_keyword(self):
        identifier_string = ""
        position_start = self.position.copy()
        
        while self.current_char != None and self.current_char in ACCEPTED_CHARS:
            identifier_string += self.current_char
            self.advance()
        
        if identifier_string in KEYWORDS_LIST:
            nominal_type = NOMINAL_TYPE_KEYWORD        
        else:
            nominal_type = NOMINAL_TYPE_IDENTIFIER
        
        return Nominal(nominal_type, identifier_string, position_start, self.position)

    def make_nominals(self):
        nominals = []

        while self.current_char != None:
            if self.current_char in IGNORED_CHARS:
                self.advance()
            if self.current_char in DIGITS:
                nominal = self.make_number()
                nominals.append(nominal)
            elif self.current_char in LETTERS:
                nominal = self.make_identifier_or_keyword()
                nominals.append(nominal)
            elif self.current_char == "+":
                nominals.append(Nominal(NOMINAL_TYPE_PLUS, position_start=self.position))
                self.advance()
            elif self.current_char == "-":
                nominals.append(Nominal(NOMINAL_TYPE_MINUS, position_start=self.position))
                self.advance()
            elif self.current_char == "*":
                nominals.append(Nominal(NOMINAL_TYPE_MULTIPLY, position_start=self.position))
                self.advance()
            elif self.current_char == "/":
                nominals.append(Nominal(NOMINAL_TYPE_DIVIDE, position_start=self.position))
                self.advance()
            elif self.current_char == "^":
                nominals.append(Nominal(NOMINAL_TYPE_POWER, position_start=self.position))
                self.advance()
            elif self.current_char == "(":
                nominals.append(Nominal(NOMINAL_TYPE_LEFT_PARENTESIS, position_start=self.position))
                self.advance()
            elif self.current_char == ")":
                nominals.append(Nominal(NOMINAL_TYPE_RIGHT_PARENTESIS, position_start=self.position))
                self.advance()
            elif self.current_char == "=":
                nominals.append(Nominal(NOMINAL_TYPE_EQUALS, position_start=self.position))
                self.advance()
            elif self.current_char == PRINT:
                nominals.append(Nominal(NOMINAL_TYPE_PRINT, position_start=self.position))
                self.advance()
            
            else:
                position_start = self.position.copy()
                char = self.current_char
                self.advance()
                return [], IllegaCharError(position_start, self.position, f"Illegal Char: [{char}]")

        nominals.append(Nominal(NOMINAL_TYPE_EOF, position_start=self.position))
        return nominals, None

from const import *
from errors import *
from position import Position
from token import Token

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
            return Token(TOKEN_TYPE_INTEGER, int(num_str), position_start, self.position)
        else:
            return Token(TOKEN_TYPE_FLOAT, float(num_str), position_start, self.position)

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in IGNORED_CHARS:
                self.advance()
            if self.current_char in DIGITS:
                token = self.make_number()
                tokens.append(token)
            elif self.current_char == "+":
                tokens.append(Token(TOKEN_TYPE_PLUS, position_start=self.position))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TOKEN_TYPE_MINUS, position_start=self.position))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TOKEN_TYPE_MULTIPLY, position_start=self.position))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TOKEN_TYPE_DIVIDE, position_start=self.position))
                self.advance()
            elif self.current_char == "^":
                tokens.append(Token(TOKEN_TYPE_POWER, position_start=self.position))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TOKEN_TYPE_LEFT_PARENTESIS, position_start=self.position))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TOKEN_TYPE_RIGHT_PARENTESIS, position_start=self.position))
                self.advance()
            else:
                position_start = self.position.copy()
                char = self.current_char
                self.advance()
                return [], IllegaCharError(position_start, self.position, f"Illegal Char: [{char}]")

        tokens.append(Token(TOKEN_TYPE_EOF, position_start=self.position))
        return tokens, None

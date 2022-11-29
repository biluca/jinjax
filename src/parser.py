from const import *
from nodes import NumberNode, BinaryOperationNode, UnaryOperationNode
from errors import InvalidSyntaxError

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.token_index = -1
        self.advance()
    
    def parse(self):
        result = self.expression()
        if not result.error and self.current_token.type != TOKEN_TYPE_EOF:
            error = InvalidSyntaxError(self.current_token.position_start, self.current_token.position_end, "+, -, * or / expected.")
            return result.failure(error)
        return result
    
    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def factor(self):
        result = ParseResult()
        token = self.current_token
        
        if token.type in (TOKEN_TYPE_PLUS, TOKEN_TYPE_MINUS):
            result.register(self.advance())
            factor = result.register(self.factor())
            if result.error:
                return result
            unaryOperationNode = UnaryOperationNode(token, factor)
            return result.success(unaryOperationNode)
        
        elif token.type in (TOKEN_TYPE_INTEGER, TOKEN_TYPE_FLOAT):
            result.register(self.advance())
            return result.success(NumberNode(token))
        
        elif token.type == TOKEN_TYPE_LEFT_PARENTESIS:
            result.register(self.advance())
            expression = result.register(self.expression())
            if result.error:
                return result
            if self.current_token.type == TOKEN_TYPE_RIGHT_PARENTESIS:
                result.register(self.advance())
                return result.success(expression)
            else:
                error = InvalidSyntaxError(self.current_token.position_start, self.current_token.position_end, ") expected.")
                return result.failure(error)
            
        error = InvalidSyntaxError(token.position_start, token.position_end, "int or float expected.")
        return result.failure(error)

    def term(self):
        return self.make_binary_operation(self.factor, (TOKEN_TYPE_MULTIPLY, TOKEN_TYPE_DIVIDE, TOKEN_TYPE_POWER))
               
    def expression(self):
        return self.make_binary_operation(self.term, (TOKEN_TYPE_PLUS, TOKEN_TYPE_MINUS))
    
    def make_binary_operation(self, function, operators):
        result = ParseResult()
        left_node = result.register(function())
        if result.error:
            return result
        
        while self.current_token.type in operators:
            operator_token = self.current_token
            result.register(self.advance())
            right_node = result.register(function())
            if result.error:
                return result
            left_node = BinaryOperationNode(left_node, operator_token, right_node)
        
        return result.success(left_node)


class ParseResult:
    
    def __init__(self) -> None:
        self.error = None
        self.node = None
    
    def register(self, result):
        if isinstance(result, ParseResult):
            if result.error:
                self.error = result.error
            return result.node
        return result
    

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self
from const import *
from nodes import NumberNode, BinaryOperationNode, UnaryOperationNode
from errors import InvalidSyntaxError


class Parser:
    def __init__(self, nominals) -> None:
        self.nominals = nominals
        self.nominal_index = -1
        self.advance()

    def parse(self):
        result = self.expression()
        if not result.error and self.current_nominal.type != NOMINAL_TYPE_EOF:
            error = InvalidSyntaxError(
                self.current_nominal.position_start,
                self.current_nominal.position_end,
                "+, -, * or / expected.",
            )
            return result.failure(error)
        return result

    def advance(self):
        self.nominal_index += 1
        if self.nominal_index < len(self.nominals):
            self.current_nominal = self.nominals[self.nominal_index]
        return self.current_nominal

    def factor(self):
        result = ParseResult()
        nominal = self.current_nominal

        if nominal.type in (NOMINAL_TYPE_PLUS, NOMINAL_TYPE_MINUS):
            result.register(self.advance())
            factor = result.register(self.factor())
            if result.error:
                return result
            unaryOperationNode = UnaryOperationNode(nominal, factor)
            return result.success(unaryOperationNode)

        elif nominal.type in (NOMINAL_TYPE_INTEGER, NOMINAL_TYPE_FLOAT):
            result.register(self.advance())
            return result.success(NumberNode(nominal))

        elif nominal.type == NOMINAL_TYPE_LEFT_PARENTESIS:
            result.register(self.advance())
            expression = result.register(self.expression())
            if result.error:
                return result
            if self.current_nominal.type == NOMINAL_TYPE_RIGHT_PARENTESIS:
                result.register(self.advance())
                return result.success(expression)
            else:
                error = InvalidSyntaxError(
                    self.current_nominal.position_start,
                    self.current_nominal.position_end,
                    ") expected.",
                )
                return result.failure(error)

        error = InvalidSyntaxError(
            nominal.position_start, nominal.position_end, "int or float expected."
        )
        return result.failure(error)

    def term(self):
        return self.make_binary_operation(
            self.factor,
            (NOMINAL_TYPE_MULTIPLY, NOMINAL_TYPE_DIVIDE, NOMINAL_TYPE_POWER),
        )

    def expression(self):
        result = ParseResult()
        if self.current_nominal.is_keyword():
            if self.current_nominal.matches(VARIABLE):
                result.register(self.advance())

            if not self.current_nominal.is_from_types(
                NOMINAL_TYPE_IDENTIFIER, NOMINAL_TYPE_EQUALS
            ):
                error = InvalidSyntaxError(
                    self.current_nominal.position_start,
                    self.current_nominal.position_end,
                    "identifier or equals expected.",
                )
                return result.failure(error)

            if self.current_nominal.is_from_type(NOMINAL_TYPE_IDENTIFIER):
                var_name = self.current_nominal
                result.register(self.advance())

            if self.current_nominal.is_from_type(NOMINAL_TYPE_EQUALS):
                result.register(self.advance())

            expression = result.register(self.expression())
            if result.error:
                return result
            return result.success(VarAssignNode(var_name, expression))

        return self.make_binary_operation(
            self.term, (NOMINAL_TYPE_PLUS, NOMINAL_TYPE_MINUS)
        )

    def make_binary_operation(self, function, operators):
        result = ParseResult()
        left_node = result.register(function())
        if result.error:
            return result

        while self.current_nominal.type in operators:
            operator_nominal = self.current_nominal
            result.register(self.advance())
            right_node = result.register(function())
            if result.error:
                return result
            left_node = BinaryOperationNode(left_node, operator_nominal, right_node)

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

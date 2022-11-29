from number import Number, ResultNumber
from const import *

class Interpreter:
    
    def __init__(self) -> None:
        pass
    
    def visit(self, node, context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)
    
    def no_visit_method(self, node, context):
        raise Exception(f"No Visit Method was Found: visit_{type(node).__name__}")
    
    def visit_NumberNode(self, node, context):
        number = Number(node.token.value)
        number.set_position(node.position_start, node.position_end)
        number.set_context(context)
        result_number = ResultNumber().success(number)
        return result_number
    
    def visit_BinaryOperationNode(self, node, context):
       
        result_number = ResultNumber()
        result = None
        left_node = result_number.register(self.visit(node.left_node, context))
        if result_number.error:
            return result_number
        right_node = result_number.register(self.visit(node.right_node, context))
        if result_number.error:
            return result_number
        
        operator_token = node.operator_token
        if operator_token.type == TOKEN_TYPE_PLUS:
            result, error = left_node.add_to(right_node)
        if operator_token.type == TOKEN_TYPE_MINUS:
            result, error = left_node.subtract_by(right_node)
        if operator_token.type == TOKEN_TYPE_MULTIPLY:
            result, error = left_node.multiply_by(right_node)
        if operator_token.type == TOKEN_TYPE_DIVIDE:
            result, error = left_node.divide_by(right_node)
        
        if error:
            return result_number.failure(error)
        else:
            result.set_position(node.position_start, node.position_end)
            result.set_context(context)
            return result_number.success(result)
    
    def visit_UnaryOperationNode(self, node, context):
        result_number = ResultNumber()
        number = result_number.register(self.visit(node.node,context))
        if result_number.error:
            return result_number
        result = number
        
        operator_token = node.operator_token
        if operator_token == TOKEN_TYPE_MINUS:
            result, error = number * (-1)
        
        if error:
            return result_number.failure(error)
        else:
            result.set_position(node.position_start, node.position_end)
            result.set_context(context)
            return result_number.success(result)
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from context import Context

def run(file_name, text):
    # Generating Tokens
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()
    
    if error:
        return None, error

    # Generating the Abstract Syntax Tree - AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error
    
    # Run the Interpreter
    context = Context("Run Function")
    interpreter = Interpreter()
    result = interpreter.visit(ast.node, context)
    
    return result.value, result.error
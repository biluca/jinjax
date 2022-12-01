from lexer import Lexer
from parser import Parser


def run(file_name, text):
    # Generating Tokens
    lexer = Lexer(file_name, text)
    nominals, error = lexer.make_nominals()

    if error:
        return None, error

    print("NOMINAL COLLECTION: ", nominals)

    # Generating the Abstract Syntax Tree - AST
    parser = Parser(nominals)
    ast = parser.parse()
    if ast.error:
        return None, ast.error
    
    print("ABSTRACT SYNTAX TREE: ", ast.node)

    return None, None

import lexer
import interpreter
import _parser as parser

lex = lexer.Lexer(
    """
    set chicken to 6
    print chicken
    """
)
tokens = lex.tokenize()
parse = parser.Parser(tokens)
nodes = parse.parse()
interpret = interpreter.Interpreter(nodes)
interpret.interpret()
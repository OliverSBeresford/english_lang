class Interpreter:
    def __init__(self, ast):
        self.ast = ast

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_PrintStatement(self, node):
        value = node.value.strip('"')
        print(value)

    def interpret(self):
        for node in self.ast:
            self.visit(node)

# Example usage
# Assuming the AST is generated from the parser for the input "print 'Hello, World!'"
"""ast = [PrintStatement('"Hello, World!"')]
interpreter = Interpreter(ast)
interpreter.interpret()"""

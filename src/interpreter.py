import _parser as parser

class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.variables = dict()
        print("Abstract syntax tree", self.ast)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_PrintStatement(self, node):
        if type(node.value) == parser.Variable:
            value = self.get_variable_value(node.value.name)
        else:
            value = node.value.strip('"').strip("'")
        print(value)

    def interpret(self):
        for node in self.ast:
            self.visit(node)
            
    def get_variable_value(self, name):
        return self.variables[name]

    def visit_VariableAssignment(self, node):
        # Assume we have a dictionary called self.variables to store variable values
        print(type(node.value))
        self.variables[node.name] = node.value

    # Update the interpret method to handle variable assignments
    # When a VariableAssignment node is encountered, call visit_VariableAssignment

    # Example usage
    # Assuming the AST is generated from the parser for the input "print 'Hello, World!'"
    """ast = [PrintStatement('"Hello, World!"')]
    interpreter = Interpreter(ast)
    interpreter.interpret()"""
    # Output: Hello, World!
    def visit_IfStatement(self, node):
        variable_value = self.variables.get(node.condition[0])
        if variable_value == node.condition[1]:
            self.visit(node.true_branch)
        elif node.false_branch:
            self.visit(node.false_branch)

    def visit_LoopStatement(self, node):
        for _ in range(node.iterations):
            self.visit(node.body)

    ### Functions
    def visit_FunctionDefinition(self, node):
        self.functions[node.name] = node.body

    def visit_FunctionCall(self, node):
        if node.name in self.functions:
            self.visit(self.functions[node.name])
        else:
            raise Exception(f"Function {node.name} not defined")
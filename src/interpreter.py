from _parser import Parser

class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.variables = dict()
        # print("Abstract syntax tree", self.ast)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_PrintStatement(self, node):
        if type(node.value) == Parser.Variable:
            value = self.get_variable_value(node.value.name)
        else:
            value = node.value.strip('"').strip("'")
        print(value)

    def interpret(self):
        for node in self.ast:
            self.visit(node)
            
    def get_variable_value(self, name):
        return self.variables[name]
    
    def __repr__(self):
        return str(self.ast)

    def visit_VariableAssignment(self, node):
        # Assume we have a dictionary called self.variables to store variable values
        if isinstance(node, Parser.String):
            self.variables[node.name] = node.value
        else:
            self.variables[node.name] = self.evaluate(node.value)
        
    def evaluate(self, node):
        if isinstance(node, Parser.Number):
            return self.number(node.value)
    
        if isinstance(node, Parser.Add):
            return self.evaluate(node.LHS) + self.evaluate(node.RHS)
        
        if isinstance(node, Parser.Subtract):
            return self.evaluate(node.LHS) - self.evaluate(node.RHS)
        
        if isinstance(node, Parser.Multiply):
            return self.evaluate(node.LHS) * self.evaluate(node.RHS)
        
        if isinstance(node, Parser.Divide):
            # Handle division and prevent division by zero
            rhs = self.evaluate(node.RHS)
            if rhs == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            return self.evaluate(node.LHS) / rhs
        
        raise TypeError("Unsupported node type", type(node))
    
    def number(self, num):
        # Try to convert the string to an integer first
        try:
            value = int(num)
        except ValueError:
            # If it can't be converted to int, convert it to float
            value = float(num)
        return value

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
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        print('\033[32mTokens:', self.tokens, '\033[0m')
        self.length = len(self.tokens)
        self.pos = 0
        self.statements = []
        self.PRECEDENCE = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
        }
        self.BINARYOPS = {
            '+': self.Add,
            '-': self.Subtract,
            '*': self.Multiply,
            '/': self.Divide
        }

    def get_next_token(self):
        token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        self.pos += 1
        return token

    def parse(self):
        while self.pos < len(self.tokens):
            token = self.get_next_token()
            if token.type == 'WORD' and 'print' == token.value:
                self.statements.append(self.parse_print_statement())
            elif token.type == 'WORD' and 'set' == token.value:
                self.statements.append(self.parse_variable_assignment())
            else:
                self.error(token)
        return self.statements

    def error(self, error='Parsing error'):
        raise Exception(error)

    # Extend the Parser to handle variable assignment
    # Assume the syntax is 'set [variable_name] to [value]'
    def parse_print_statement(self):
        value_token = self.get_next_token()
        if value_token.type == 'STRING' or value_token.type == 'NUMBER':
            return self.PrintStatement(value_token.value)
        elif value_token.type == 'WORD':
            return self.PrintStatement(self.Variable(value_token.value))
        else:
            self.error()
    
    def parse_variable_assignment(self):
        variable_name_token = self.get_next_token()  # should be a variable name
        to_word = self.get_next_token()
        if to_word.type != 'WORD' or to_word.value != 'to':
            self.error('Invalid syntax when creting a variable')
        value_token = self.parse_value()  # should be a value
        return self.VariableAssignment(name=variable_name_token.value, value=value_token)

    # Update the parse method to handle variable assignment
    # Add a check for 'set' token and then call parse_variable_assignment
    def parse_value(self):
        value_token = self.get_next_token()
        if value_token.type == 'STRING':
            return self.String(str(value_token.value))
        elif value_token.type == 'NUMBER':
            self.back()
            return self.parse_expression()
        else:
            self.error()
            
    def parse_expression(self, precedence=0):
        token = self.get_next_token()
        if token.type == 'NUMBER':
            left = self.Number(token.value)
        else:
            raise SyntaxError(f'Unexpected token: {token}')
        operation = self.tokens[self.pos]

        while operation != None and operation.type == 'OPERATOR' and self.PRECEDENCE[operation.value] > precedence:
            self.pos += 1
            next_precedence = self.PRECEDENCE[operation.value]
            right = self.parse_expression(next_precedence)
            left = self.BINARYOPS[operation.value](left, right)
            operation = self.tokens[self.pos]
        
        return left
        
    # Extend the Parser to handle if statements
    # Assume a simple condition 'if [variable_name] is [value]'
    def back(self):
        self.pos -= 1
    
    def parse_if_statement(self):
        # Assuming the current token is 'if'
        self.get_next_token()  # consume 'if'
        variable_name_token = self.get_next_token()  # should be a variable name
        self.get_next_token()  # consume 'is'
        value_token = self.get_next_token()  # should be a value
        condition = (variable_name_token.value, value_token.value)
        
        # Parse the true branch (single statement for simplicity)
        true_branch = self.parse_statement()
        
        # Optionally handle else branch
        
        return self.IfStatement(condition, true_branch)


    # Extend the Parser to handle loop statements
    # Assume the syntax is 'repeat [number] times'

    def parse_loop_statement(self):
        self.get_next_token()  # consume 'repeat'
        iterations_token = self.get_next_token()  # should be a number
        iterations = int(iterations_token.value)
        self.get_next_token()  # consume 'times'
        
        # Parse the loop body (single statement for simplicity)
        body = self.parse_statement()
        
        return self.LoopStatement(iterations, body)




    # Extend the Parser to handle function definitions
    # Assume the syntax is 'define function [name] as'

    def parse_function_definition(self):
        self.get_next_token()  # consume 'define function'
        name_token = self.get_next_token()  # should be the function name
        self.get_next_token()  # consume 'as'
        
        # Parse the function body (single statement for simplicity)
        body = self.parse_statement()
        
        return self.FunctionDefinition(name_token.value, body)

    # Extend the Parser to handle function calls
    # Assume the syntax is 'call [name]'

    def parse_function_call(self):
        self.get_next_token()  # consume 'call'
        name_token = self.get_next_token()  # should be the function name
        
        return self.FunctionCall(name_token.value)
    
    class ASTNode:
        pass

    class PrintStatement(ASTNode):
        def __init__(self, value):
            self.value = value

    class Number(ASTNode):
        def __init__(self, value):
            self.value = value

    class String(ASTNode):
        def __init__(self, value):
            self.value = value
            
    class VariableAssignment(ASTNode):
        def __init__(self, name, value):
            self.name = name
            self.value = value

    class IfStatement(ASTNode):
        def __init__(self, condition, true_branch, false_branch=None):
            self.condition = condition
            self.true_branch = true_branch
            self.false_branch = false_branch

    class LoopStatement(ASTNode):
        def __init__(self, iterations, body):
            self.iterations = iterations
            self.body = body
            
    ### Functions
    class FunctionDefinition(ASTNode):
        def __init__(self, name, body):
            self.name = name
            self.body = body

    class Variable(ASTNode):
        def __init__(self, name):
            self.name = name

    class FunctionCall(ASTNode):
        def __init__(self, name):
            self.name = name
            
    class Operation(ASTNode):
        def __init__(self, LHS, RHS):
            self.LHS = LHS
            self.RHS = RHS
        
        def __repr__(self):
            return f'{self.repr}({self.type}, {self.value})'
    
    class Add(Operation):
        def __init__(self, LHS, RHS):
            super().__init__(LHS, RHS)
            self.repr = 'ADD'
    
    class Subtract(Operation):
        def __init__(self, LHS, RHS):
            super().__init__(LHS, RHS)
            self.repr = 'SUB'
    
    class Multiply(Operation):
        def __init__(self, LHS, RHS):
            super().__init__(LHS, RHS)
            self.repr = 'MULT'
    
    class Divide(Operation):
        def __init__(self, LHS, RHS):
            super().__init__(LHS, RHS)
            self.repr = 'DIV'
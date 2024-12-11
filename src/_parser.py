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

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        print("Parser tokens:", self.tokens)
        self.pos = 0
        self.statements = []

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
                self.error()
        return self.statements

    def error(self, error='Parsing error'):
        raise Exception(error)

    # Extend the Parser to handle variable assignment
    # Assume the syntax is "set [variable_name] to [value]"
    def parse_print_statement(self):
        value_token = self.get_next_token()
        if value_token.type == 'STRING' or value_token.type == 'NUMBER':
            return PrintStatement(value_token.value)
        elif value_token.type == 'WORD':
            return PrintStatement(Variable(value_token.value))
        else:
            self.error()
    
    def parse_variable_assignment(self):
        variable_name_token = self.get_next_token()  # should be a variable name
        to_word = self.get_next_token()
        if to_word.type != 'WORD' or to_word.value != 'to':
            self.error('Invalid syntax when creting a variable')
        value_token = self.parse_value()  # should be a value
        return VariableAssignment(variable_name_token.value, value_token.value)

    # Update the parse method to handle variable assignment
    # Add a check for 'set' token and then call parse_variable_assignment
    def parse_value(self):
        value_token = self.get_next_token()
        if value_token.type == 'STRING':
            return String(str(value_token.value))
        elif value_token.type == 'NUMBER':
            return Number(value_token.value)
        else:
            self.error()


    # Extend the Parser to handle if statements
    # Assume a simple condition "if [variable_name] is [value]"

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
        
        return IfStatement(condition, true_branch)




    # Extend the Parser to handle loop statements
    # Assume the syntax is "repeat [number] times"

    def parse_loop_statement(self):
        self.get_next_token()  # consume 'repeat'
        iterations_token = self.get_next_token()  # should be a number
        iterations = int(iterations_token.value)
        self.get_next_token()  # consume 'times'
        
        # Parse the loop body (single statement for simplicity)
        body = self.parse_statement()
        
        return LoopStatement(iterations, body)




    # Extend the Parser to handle function definitions
    # Assume the syntax is "define function [name] as"

    def parse_function_definition(self):
        self.get_next_token()  # consume 'define function'
        name_token = self.get_next_token()  # should be the function name
        self.get_next_token()  # consume 'as'
        
        # Parse the function body (single statement for simplicity)
        body = self.parse_statement()
        
        return FunctionDefinition(name_token.value, body)

    # Extend the Parser to handle function calls
    # Assume the syntax is "call [name]"

    def parse_function_call(self):
        self.get_next_token()  # consume 'call'
        name_token = self.get_next_token()  # should be the function name
        
        return FunctionCall(name_token.value)
class ASTNode:
    pass

class PrintStatement(ASTNode):
    def __init__(self, value):
        self.value = value

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def get_next_token(self):
        token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        self.pos += 1
        return token

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            token = self.get_next_token()
            if token.type == 'WORD' and 'print' in token.value:
                value_token = self.get_next_token()
                if value_token.type == 'WORD' or value_token.type == 'NUMBER':
                    statements.append(PrintStatement(value_token.value))
                else:
                    self.error()
            else:
                self.error()
        return statements

    def error(self):
        raise Exception('Parsing error')


class VariableAssignment(ASTNode):
    def __init__(self, variable_name, value):
        self.variable_name = variable_name
        self.value = value

# Extend the Parser to handle variable assignment
# Assume the syntax is "set [variable_name] to [value]"

def parse_variable_assignment(self):
    # Assuming the current token is 'set'
    self.get_next_token()  # consume 'set'
    variable_name_token = self.get_next_token()  # should be a variable name
    self.get_next_token()  # consume 'to'
    value_token = self.get_next_token()  # should be a value
    return VariableAssignment(variable_name_token.value, value_token.value)

# Update the parse method to handle variable assignment
# Add a check for 'set' token and then call parse_variable_assignment

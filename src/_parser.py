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

